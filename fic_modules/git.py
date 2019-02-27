"""
This module handles the git generation, filtering and other git related stuff.
"""

import json
import re
from datetime import (
    datetime,
    timedelta
)
import requests
from dateutil.parser import parse
from fic_modules.configuration import (
    LAST_MONTH,
    GIT,
    REPOSITORIES,
    WORKING_DIR,
    LOGGER
)
from fic_modules.helper_functions import (
    remove_chars,
    limit_checker,
    get_commit_details,
    compare_files
)
from fic_modules.markdown_modules import (
    generate_markdown_header,
    write_main_md_table,
    create_git_md_table,
    create_md_table_for_scriptworkers
)


def filter_git_commit_data(repository_name, repository_team, repository_type,
                           folders_to_check):
    """
    Filters out only the data that we need from a commit
    Substitute the special characters from commit message using 'sub' function
    from 're' library
    :param repository_team:
    :param repository_name: name of the given repo
    :param repository_type: type of a repo we are going to work with
    :param folders_to_check: list that contains every folder we care about
    from given repo
    :return: Filtered json data
    TODO: please add the exception blocks since the script fails when it can't
    pull a data:
    (e.g raise self.__createException(status, responseHeaders, output)
    github.GithubException.GithubException: 502 {'message': 'Server Error'}
    """

    repository_path = repository_team + repository_name
    # TYPE = NO-TAG
    if repository_type == "no-tag":
        filter_git_no_tag(repository_name, repository_path, folders_to_check)
    # TYPE = COMMIT-KEYWORD
    if repository_type == "commit-keyword":
        filter_git_commit_keyword(repository_name, repository_path)
    # TYPE = TAG
    if repository_type == "tag":
        if repository_name == "build-puppet":
            filter_git_tag_bp(repository_name,
                              repository_team,
                              repository_path)
        elif repository_name != "build-puppet":
            filter_git_tag(repository_name, repository_team, repository_path)


def create_files_for_git(repositories_holder, onerepo):
    """
    Main GIT function. Takes every Git repo from a .json file which is
    populated with repositories and writes all the commit data of each repo in
    a. creates a json and MD file for each repo as well.
    :param: repositories_holder: Expects a .json file that contains a list of
    repositories.
    :return: The end result is a .json and a .md file for every git repository.
    Can be found inside git_files/
    """
    if onerepo:
        repository_team = REPOSITORIES \
            .get("Github") \
            .get(repositories_holder) \
            .get("team")
        repository_type = REPOSITORIES \
            .get("Github") \
            .get(repositories_holder) \
            .get("configuration") \
            .get("type")
        LOGGER.info("Working on repo: {}".format(repositories_holder))
        folders_to_check = [folder for folder in REPOSITORIES
                            .get("Github")
                            .get(repositories_holder)
                            .get("configuration")
                            .get("folders-to-check")]
        filter_git_commit_data(repositories_holder,
                               repository_team,
                               repository_type,
                               folders_to_check)
        if repositories_holder == "build-puppet":
            create_git_md_table(repositories_holder, "git_files")
            create_md_table_for_scriptworkers(repositories_holder)
        else:
            create_git_md_table(repositories_holder, "git_files")
        LOGGER.info("MD table generated successfully for {}"
                    .format(repositories_holder))
    else:
        for repo in repositories_holder["Github"]:
            repository_name = repo
            repository_team = repositories_holder \
                .get("Github") \
                .get(repo) \
                .get("team")
            repository_type = repositories_holder \
                .get("Github") \
                .get(repo) \
                .get("configuration") \
                .get("type")
            LOGGER.info("Working on repo: {}".format(repository_name))
            folders_to_check = [folder for folder in repositories_holder
                                .get("Github")
                                .get(repo)
                                .get("configuration")
                                .get("folders-to-check")]
            filter_git_commit_data(repository_name,
                                   repository_team,
                                   repository_type,
                                   folders_to_check)
            if repository_name == "build-puppet":
                create_git_md_table(repository_name, "git_files")
                create_md_table_for_scriptworkers(repository_name)
            else:
                create_git_md_table(repository_name, "git_files")
            LOGGER.info("MD table generated successfully")
            LOGGER.info("Finished working on {}".format(repository_name))


def filter_git_tag_bp(repository_name, repository_team, repository_path):
    """
    Filters out only the data that we need from a commit
    Substitute the special characters from commit message using 'sub' function
    from 're' library
    :param repository_team: the team of the given repo
    :param repository_name: name of the given repo
    :param repository_path:
    :return: the commits into a dictionary
    TODO: please add the exception blocks since the script fails when it can't
    pull a data:
    (e.g raise self.__createException(status, responseHeaders, output)
    github.GithubException.GithubException: 502 {'message': 'Server Error'}
    """
    number = 0
    commit_number_tracker = 1
    pathway = REPOSITORIES.get("Github") \
        .get(repository_name) \
        .get("configuration") \
        .get("files-to-check")
    last_checked = last_check(repository_name)
    new_commit_dict = {"0": {"lastChecked": str(datetime.utcnow())}}

    if limit_checker():
        new_commits = GIT.get_repo(repository_path) \
                         .get_commits(since=last_checked)

    for commit in new_commits:
        each_commit = {}
        switch = False
        LOGGER.info("Commit number: " + str(commit_number_tracker))
        commit_number_tracker += 1
        files_changed_by_commit = [x.filename for x in commit.files]
        LOGGER.info(files_changed_by_commit)
        LOGGER.info(len(files_changed_by_commit))
        changed_file_number = 1
        for entry in files_changed_by_commit:
            LOGGER.info("changed file number: {} "
                        .format(changed_file_number))
            LOGGER.info(entry)
            changed_file_number += 1
            for scriptworkers in pathway:
                LOGGER.info("checking repo:{} ".format(scriptworkers))
                if entry in pathway[scriptworkers]:
                    LOGGER.debug(scriptworkers, " needs to be checked.")
                    scriptworker_repo = scriptworkers
                    version_path = REPOSITORIES.get("Github") \
                        .get("build-puppet") \
                        .get("configuration") \
                        .get("files-to-check") \
                        .get(scriptworker_repo)
                    latest_releases = get_version(scriptworker_repo,
                                                  repository_team)
                    version_comparison_result = compare_versions(
                        version_path,
                        scriptworker_repo,
                        latest_releases)

                    if version_comparison_result:
                        switch = True
                        new_scriptworker_dict = filter_git_scriptworkers(
                            latest_releases,
                            repository_team,
                            scriptworker_repo)
                        json_writer_git(scriptworker_repo,
                                        new_scriptworker_dict)
                    else:
                        LOGGER.info("No new changes entered production")
        if switch:
            number += 1
            each_commit.update({int(number): get_commit_details(commit)})
            new_commit_dict.update(each_commit)
    json_writer_git(repository_name, new_commit_dict)


def filter_git_scriptworkers(latest_releases, repo_team, script_repo):
    """
    filters the scriptworker repos that are under build-puppet
    :param latest_releases: data about last release
    :param repo_team: team name as a string
    :param script_repo: scriptworker repo we are working on
    :return: returns the new commits of a repo
    """
    last_local_date = get_date_from_json(script_repo)
    new_commit_version_date = \
        datetime.strptime(latest_releases
                          .get("latest_release")
                          .get("date"),
                          "%Y-%m-%d %H:%M:%S")
    commit_number = 0
    new_scriptworker_dict = {
        (int(commit_number)): {"lastChecked": str(datetime.utcnow()),
                               "last_releases": latest_releases}}
    new_repo_path = repo_team + script_repo
    for commit2 in GIT.get_repo(new_repo_path).get_commits(
            since=last_local_date):
        last_modified = \
            datetime.strftime(parse(commit2.last_modified),
                              "%Y-%m-%d %H:%M:%S")
        last_modified = datetime.strptime(last_modified,
                                          "%Y-%m-%d %H:%M:%S")
        if last_modified <= new_commit_version_date:
            each_commit2 = {}
            commit_number += 1
            commit_details = get_commit_details(commit2)
            each_commit2.update({int(commit_number): commit_details})
            new_scriptworker_dict.update(each_commit2)
    return new_scriptworker_dict


def filter_git_tag(repository_name, repository_team, repository_path):
    """
    Filters out only the data that we need from a commit
    Substitute the special characters from commit message using 'sub' function
    from 're' library
    :param repository_team: the team of the given repo
    :param repository_name: name of the given repo
    :param repository_path:
    :return: the commits into a dictionary
    TODO: please add the exception blocks since the script fails when it can't
    pull a data:
    (e.g raise self.__createException(status, responseHeaders, output)
     github.GithubException.GithubException: 502 {'message': 'Server Error'}
    """
    number = 0

    latest_releases = get_version(repository_name, repository_team)
    if get_version_from_json(repository_name) == \
            latest_releases.get("latest_release").get("version"):
        LOGGER.info("No new changes entered production")
    else:
        last_commit_date = get_date_from_json(repository_name)
        new_version_commit_date = datetime.strptime(latest_releases
                                                    .get("latest_release")
                                                    .get("date"),
                                                    "%Y-%m-%d %H:%M:%S")
        new_commit_dict = {"0": {"lastChecked": str(datetime.utcnow()),
                                 "last_releases": latest_releases}}
        for commit in GIT.get_repo(repository_path) \
                         .get_commits(since=last_commit_date):
            last_modified = datetime.strftime(parse(commit.last_modified),
                                              "%Y-%m-%d %H:%M:%S")
            last_modified = datetime.strptime(last_modified,
                                              "%Y-%m-%d %H:%M:%S")
            if last_modified <= new_version_commit_date:
                each_commit = {}
                number += 1
                each_commit.update({int(number): get_commit_details(commit)})
                new_commit_dict.update(each_commit)
        json_writer_git(repository_name, new_commit_dict)


def get_version(repo_name, repo_team):
    """
    :param repo_name: repository name
    :param repo_team: repository team
    :return: a dictionary with information from the last two release version:
     latestRelease and previousRelease
    """
    repo_path = repo_team + repo_name
    iteration = 0
    empty_dict = {}
    for tags in GIT.get_repo(repo_path).get_tags():
        version = tags.name
        sha = tags.commit.sha
        date = tags.commit.commit.last_modified
        date_format = parse(date)
        date = date_format.strftime("%Y-%m-%d %H:%M:%S")
        author = tags.commit.author.login
        if iteration == 0:
            latest_release = {"version": version,
                              "sha": sha,
                              "date": date,
                              "author": author
                              }
            empty_dict.update({"latest_release": latest_release})
            break
    return empty_dict


def get_version_from_build_puppet(version_path, repo_name):
    """
    :param: version_path: Path to the requierments.txt where the version number
     is stored
    :param: repo_name: The repo for which we are checking the version.
    :return: Returns the version number that is stored in build-puppet for
    each *scriptworker
    """
    file_to_string = requests.get(version_path).text.split()
    for word in file_to_string:
        if repo_name in word:
            version_in_puppet = re.split("\\b==\\b", word)[-1]
            if version_in_puppet != repo_name:
                return version_in_puppet


def json_writer_git(repository_name, new_commits):
    """
    :param repository_name:
    :param new_commits: a dictionary with the new commits
    :return: write the json file with the old and the new commits
    """
    git_json_filename = "{}.json".format(repository_name)
    try:
        with open(WORKING_DIR + "/git_files/" + git_json_filename, "r") as \
                commit_json:
            json_content = json.load(commit_json)
    except FileNotFoundError:
        json_content = ""
    if len(json_content) > 1:
        number = len(new_commits) - 1
        for old_commit in json_content:
            if old_commit != "0":
                number += 1
                new_commits.update({int(number): json_content[old_commit]})

    if new_commits:
        json_file = open(WORKING_DIR + "/git_files/" + git_json_filename, "w")
        json.dump(new_commits, json_file, indent=2)
        json_file.close()
        try:
            del new_commits["0"]
        except KeyError:
            pass
        try:
            with open("changelog.json", "r") as file:
                data = json.load(file)
            data[repository_name] = new_commits
        except json.decoder.JSONDecodeError:
            data = {}
            data.update({repository_name: new_commits})
        with open("changelog.json", "w") as file:
            json.dump(data, file, indent=2)


def last_check(repository_name):
    """

    :param repository_name:
    :return: the last time when the repository was checked
    """
    git_json_filename = "{}.json".format(repository_name)
    try:
        with open(WORKING_DIR + "/git_files/" + git_json_filename, "r") as \
                commit_json:
            json_content = json.load(commit_json)
            try:
                last_checked = datetime.strptime(json_content
                                                 .get("0")
                                                 .get("lastChecked"),
                                                 "%Y-%m-%d %H:%M:%S")
                LOGGER.info("Repo last updated on: " + str(last_checked))

            except ValueError:
                last_checked = datetime.strptime(json_content
                                                 .get("0")
                                                 .get("lastChecked"),
                                                 "%Y-%m-%d %H:%M:%S.%f")
                LOGGER.info("Repo last updated on: " + str(last_checked))

    except IOError:
        last_checked = LAST_MONTH
    return last_checked


def get_version_from_json(repo_name):
    """
    :param repo_name: name of the repo we are working on
    :return: version our repo was bumped to by the last local commit that we
    have
    """
    git_json_filename = "{}.json".format(repo_name)
    try:
        with open(WORKING_DIR + "/git_files/" + git_json_filename, "r") as \
                commit_json:
            json_content = json.load(commit_json)
        last_stored_version = json_content \
            .get("0") \
            .get("last_releases") \
            .get("latest_release") \
            .get("version")
    except FileNotFoundError:
        last_stored_version = ""
    return last_stored_version


def get_date_from_json(repo_name):
    """
    :param repo_name: name of the repo we are currently working on
    :return: date of the last commit that we have locally in our json
    """
    git_json_filename = "{}.json".format(repo_name)
    try:
        with open(WORKING_DIR + "/git_files/" + git_json_filename, "r") as \
                commit_json:
            json_content = json.load(commit_json)
        last_stored_date = json_content \
            .get("0") \
            .get("last_releases") \
            .get("latest_release") \
            .get("date")
        date_format = parse(last_stored_date)
        last_stored_date = datetime.strptime(str(date_format),
                                             "%Y-%m-%d %H:%M:%S")
    except FileNotFoundError:
        last_stored_date = datetime.strptime("2019-01-01 01:00:00",
                                             "%Y-%m-%d %H:%M:%S")
        LOGGER.info("last local date was: {} ".format(last_stored_date))
    return last_stored_date


def filter_git_no_tag(repository_name, repository_path, folders_to_check):
    """
    Filters out only the data that we need from a commit
    Substitute the special characters from commit message using 'sub' function
     from 're' library
    :param repository_name: name of the given repo
    :param repository_path:
    :param folders_to_check: the folders we care about
    :return: the commits into a dictionary
    TODO: please add the exception blocks since the script fails when it
    can't pull a data:
    (e.g raise self.__createException(status, responseHeaders, output)
    github.GithubException.GithubException: 502 {'message': 'Server Error'}
    """
    number = 0
    last_checked = last_check(repository_name)
    new_commit_dict = {"0": {"lastChecked": str(datetime.utcnow())}}
    if limit_checker():
        new_commits = GIT.get_repo(repository_path) \
                         .get_commits(since=last_checked)

    for commit in new_commits:
        each_commit = {}
        if folders_to_check:
            files_changed = []
            for entry in commit.files:
                files_changed.append(entry.filename)
            if compare_files(files_changed, folders_to_check):
                number += 1
                each_commit.update({int(number): get_commit_details(commit)})
                new_commit_dict.update(each_commit)
        else:
            number += 1
            each_commit.update({int(number): get_commit_details(commit)})
            new_commit_dict.update(each_commit)
    json_writer_git(repository_name, new_commit_dict)
    return True


def filter_git_commit_keyword(repository_name, repository_path):
    """
    Filters out only the data that we need from a commit
    Substitute the special characters from commit message using 'sub' function
    from 're' library
    :param repository_name: name of the given repo
    :param repository_path:
    :return: the commits into a dictionary
    TODO: please add the exception blocks since the script fails when it can't
    pull a data:
    (e.g raise self.__createException(status, responseHeaders, output)
    github.GithubException.GithubException: 502 {'message': 'Server Error'}
    """
    number = 0
    last_checked = last_check(repository_name)
    new_commit_dict = {"0": {"lastChecked": str(datetime.utcnow())}}
    if limit_checker():
        new_commits = GIT.get_repo(repository_path) \
                         .get_commits(since=last_checked)

    for commit in new_commits:
        files_changed_by_commit = [x.filename for x in commit.files]
        if files_changed_by_commit:
            each_commit = {}
            LOGGER.info(commit.commit.message)
            if "deploy" in commit.commit.message:
                number += 1
                each_commit.update({int(number): get_commit_details(commit)})
                new_commit_dict.update(each_commit)
    json_writer_git(repository_name, new_commit_dict)


def compare_versions(version_path, scriptworker_repo, latest_releases):
    """
    checks the version of a scriptworker repo from its changelog, build-puppet
    and locally saved one against each other
    :param version_path:
    :param scriptworker_repo:
    :param latest_releases:
    :return:
    """

    version_in_puppet = get_version_from_build_puppet(version_path,
                                                      scriptworker_repo)
    last_local_version = get_version_from_json(scriptworker_repo)

    if version_in_puppet == latest_releases.get("latest_release") \
            .get("version"):
        if version_in_puppet != last_local_version:
            return True
        else:
            return False
    else:
        return True


def extract_json_from_git(json_files, path_to_files, days_to_generate):
    """
    Extracts the json data from json files and writes the data to the main
    markdown table file.
    The function looks into json files after the last commit, extracts it and
    calls the write_main_md_table function.
    :param days_to_generate:
    :param json_files: List of files to extract commits from.
    :param path_to_files: Folder to json files
    :return: none
    """

    time_24h_ago = datetime.utcnow() - timedelta(days=days_to_generate)
    test = datetime.strftime(time_24h_ago, "%Y-%m-%d %H:%M:%S")
    time_24h_ago = datetime.strptime(test, "%Y-%m-%d %H:%M:%S")

    for file in json_files:
        file_path = "{}/".format(path_to_files) + file
        count_pushes = 0
        with open(file_path) as json_file:
            data = json.load(json_file)
            base_link = "https://github.com/mozilla-releng/firefox-infra-" \
                        "changelog/blob/master/{}/" \
                        .format(path_to_files)
            repository_url = base_link + file \
                .rstrip() \
                .replace(" ", "%20") \
                .rstrip() \
                .replace(".json", ".md")
            repository_json = base_link + file \
                .rstrip() \
                .replace(" ", "%20")
            repository_title = file.replace(".json", "")
            try:
                generate_markdown_header("changelog.md",
                                         repository_title,
                                         repository_url,
                                         repository_json)
                if "0" in data:
                    del data["0"]
                for commit_iterator in data:
                    commit_number = str(commit_iterator)
                    commit_date = data.get(commit_number).get("commit_date")
                    is_it_under_24 = datetime.strptime(commit_date,
                                                       "%Y-%m-%d %H:%M:%S")
                    if is_it_under_24 > time_24h_ago:
                        count_pushes = count_pushes + 1
                        commit_description = data \
                            .get(commit_number) \
                            .get("commit_message")
                        commit_description = remove_chars(commit_description,
                                                          "\U0001f60b")
                        commit_url = data.get(commit_number).get("url")
                        commit_url = "[Link](" + commit_url + ")"
                        author = data.get(commit_number).get("commiter_name")
                        review = "N/A"
                        write_main_md_table("changelog.md",
                                            commit_url,
                                            commit_description,
                                            author,
                                            review,
                                            commit_date)
                if count_pushes == 0:
                    commit_url = " "
                    if days_to_generate == 1:
                        commit_description = "No push in the last day.. " \
                                             "[see the history of MD " \
                                             "commits](" + \
                                             repository_url + \
                                             ")"
                    else:
                        commit_description = "No push in the last " + \
                                             str(days_to_generate) + \
                                             " days.. [see the history of MD" \
                                             " commits](" + \
                                             repository_url + \
                                             ")"
                    author = "FIC - BOT"
                    review = "Self Generated"
                    commit_date = " - "
                    write_main_md_table("changelog.md",
                                        commit_url,
                                        commit_description,
                                        author,
                                        review,
                                        commit_date)
            except KeyError:
                LOGGER.info("File " + file + " is empty. \nPlease check:" +
                            str(repository_url) + " for more details.\n")