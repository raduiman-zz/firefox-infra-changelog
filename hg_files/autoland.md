## AUTOLAND COMMIT MARKDOWN TABLE SINCE 2018-11-13 18:17:15.415335

| Commit Number | Commiter | Commit Message | Node | Date | 
|:---:|:----:|:----------------------------------:|:------:|:----:| 
|19|Robert Strong <robert.bugzilla@gmail.com>|Bug 1508637 - Update comments in removed-files.in. r=mhowell  Removed comment about Firefox 27 and below since it is no longer relevant after the LZMA watershed Changed a couple of comments for clarity  Differential Revision: https://phabricator.services.mozilla.com/D12424|24cd301f1e439e414c178fd6f404894d44270e34|2018-11-20 18:04:42
|18|Patrick Brosset <pbrosset@mozilla.com>|Bug 1508581 - Fix a few UI inconsistencies in the flex inspector in RTL; r=miker  Differential Revision: https://phabricator.services.mozilla.com/D12418|e14fb4f0ce8268b4aee4ab20d791dded24379db8|2018-11-20 16:44:28
|17|Julian Descottes <jdescottes@mozilla.com>|Bug 1493968 - Wait for requests to finish in aboutdebugging navigate test;r=ladybenko  Still not sure what is the root issue here, but none of the regular connect tests are failing so I think the issue occurs when we remove tabs in the second step.  Differential Revision: https://phabricator.services.mozilla.com/D12332|e71f2bd051cf58c2fa805d8dce0032a6c5e77af8|2018-11-20 17:38:27
|16|Iain Ireland <iireland@mozilla.com>|Bug 1497107: Add ensureBallast call to freezePropertiesForCommonPrototype r=nbp  Differential Revision: https://phabricator.services.mozilla.com/D12184|136188d4f9281e3cec98699de83accbb0ad79439|2018-11-19 14:54:06
|15|Ted Campbell <tcampbell@mozilla.com>|Bug 1508255 - Merge js/src/.clang-format into top-level r=sylvestre  The style options now match, so remove js/src/.clang-format \o/  Depends on D12391  Differential Revision: https://phabricator.services.mozilla.com/D12392|2d8d64aff05a9af6af00a99c7922b86ad9d1bb55|2018-11-20 14:42:30
|14|Ted Campbell <tcampbell@mozilla.com>|Bug 1508255 - Allow clang-format to reflow comments in js/src r=jandem,arai  Previous patches on this bug fix sources of bad comment reflow. This patch changes the option in js/src/.clang-format. Doing this puts SpiderMonkey in-line with Gecko and generates better results from clang-format.  Depends on D12390  Differential Revision: https://phabricator.services.mozilla.com/D12391|d437391bafa1ec497443aedac9500cbfa172ec26|2018-11-20 13:43:42
|13|Ted Campbell <tcampbell@mozilla.com>|Bug 1508255 - Wrap ES Spec reference comments r=jorendorff  Depends on D12389  Differential Revision: https://phabricator.services.mozilla.com/D12390|fa3eaa0d2cde35eb9435f6f8455148f9eec5ff4f|2018-11-20 12:53:32
|12|Ted Campbell <tcampbell@mozilla.com>|Bug 1508255 - Reformat comments in js/src/Stream.cpp r=jorendorff  This generates much better results for clang-format.  Differential Revision: https://phabricator.services.mozilla.com/D12389|5219139e6d0f9fb6c9effc4df73244b8f9dd418c|2018-11-20 17:21:06
|11|Ted Campbell <tcampbell@mozilla.com>|Bug 1508255 - More formatting changes in js/src r=jandem  These also help the clang-format result but are more subjective.  Depends on D12387  Differential Revision: https://phabricator.services.mozilla.com/D12388|32eadea53faa9aca578c11bf682fcbb9385f9ebf|2018-11-20 12:23:38
|10|Ted Campbell <tcampbell@mozilla.com>|Bug 1508255 - Minor formatting changes in js/src r=jandem  These cause clang-format to generate better results when reflowing comments.  Depends on D12386  Differential Revision: https://phabricator.services.mozilla.com/D12387|ba2da67c9e7e7541e4be66e5841c3a115c31ba1e|2018-11-20 12:15:12
|9|Ted Campbell <tcampbell@mozilla.com>|Bug 1508255 - Truncate '   ' lines in js/src comments r=jandem  Depends on D12385  Differential Revision: https://phabricator.services.mozilla.com/D12386|cf2b7ca307b68da20bfdd196e8dc1a4e99e62a2d|2018-11-20 12:07:16
|8|Ted Campbell <tcampbell@mozilla.com>|Bug 1508255 - Use |clang-format off| for some js/src comments r=jandem  These comments get mangled by clang-format so use |clang-format off| around them for now. In the future they can be rewritten if desired.  Differential Revision: https://phabricator.services.mozilla.com/D12385|c86b9e22b393d97c6d4e4dc0fc33bc6cd3c2172c|2018-11-20 12:06:02
|7|Razvan Caliman <rcaliman@mozilla.com>|Bug 1507749 - Account for changing TextProperty when editing inline styles. r=pbro  The patch for https://bugzilla.mozilla.org/show_bug.cgi?id=1467076 discards previous TextProperty instances for the element's inline style when the inline style is updated.  On start, the Shape Path Editor kept a reference to the original TextProperty instance. This outdated instance caused the update mechanism of the Shape Path Editor to fail.  This patch fixes the issue by keeping metadata (index and property name) about the TextProperty to re-identify the correct one when needed instead of relying on a potentially outdated reference.  Differential Revision: https://phabricator.services.mozilla.com/D12157|4b78e1686da9ba317be1796cf241db3231f9cb75|2018-11-20 17:19:47
|6|Csoregi Natalia <ncsoregi@mozilla.com>|Backed out 6 changesets (bug 1493292) for bustage on /nsTransferable.cpp. CLOSED TREE  Backed out changeset f198bf91320b (bug 1493292) Backed out changeset 6487aa307123 (bug 1493292) Backed out changeset f2cabd69c568 (bug 1493292) Backed out changeset 71430fceb4a3 (bug 1493292) Backed out changeset 3a9b6d65d8c7 (bug 1493292) Backed out changeset 55769869037c (bug 1493292)|4b0554a10847e9a879ab193bf16a3bbdaa8e69d4|2018-11-20 17:13:18
|5|Jan de Mooij <jdemooij@mozilla.com>|Bug 1508605 - Change some comments from /   / to // to avoid clang-format issues. r=tcampbell  Differential Revision: https://phabricator.services.mozilla.com/D12416|5bad4fe7108eda1ca69c5f5aac82b4042c874deb|2018-11-20 16:47:07
|4|Tom Schuster <evilpies@gmail.com>|Bug 1493292 - Remove len from nsIFormatConverter. r=smaug  Depends on D11204  Differential Revision: https://phabricator.services.mozilla.com/D11205|f198bf91320bf774f2c9f204c426ac0c2da95aa2|2018-11-20 16:47:13
|3|Tom Schuster <evilpies@gmail.com>|Bug 1493292 - Remove len from nsIFlavorDataProvider r=smaug  Depends on D11203  Differential Revision: https://phabricator.services.mozilla.com/D11204|6487aa307123e63554a714e0cece6273e57017b1|2018-11-20 16:47:11
|2|Tom Schuster <evilpies@gmail.com>|Bug 1493292 - Remove len from nsTransferable. r=smaug  Depends on D11202  Differential Revision: https://phabricator.services.mozilla.com/D11203|f2cabd69c568bd5e6f50f7f3f5d6f5d55c6b7222|2018-11-20 16:47:09
|1|Tom Schuster <evilpies@gmail.com>|Bug 1493292 - Remove aDataLen parameters from nsITransferable.setTransferData. r=smaug  Depends on D11201  Differential Revision: https://phabricator.services.mozilla.com/D11202|71430fceb4a3f1641b2d786e4f66e83c87149946|2018-11-20 16:47:04
|0|Tom Schuster <evilpies@gmail.com>|Bug 1493292 - Remove aDataLen parameters from nsITransferable.getTransferData. r=smaug  Depends on D11200  Differential Revision: https://phabricator.services.mozilla.com/D11201|3a9b6d65d8c7afb9289b1eca8dbaf84e5da37c69|2018-11-20 16:47:02

