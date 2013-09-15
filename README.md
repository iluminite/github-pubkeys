github-pubkeys
==============

Simple python script to manage (list/create/delete) SSH public keys in your Github account via the Github API

* grab ![the script](https://raw.github.com/illumin-us-r3v0lution/github-pubkeys/master/github_keys.py) with `wget`:

    root@oms:~# wget https://raw.github.com/illumin-us-r3v0lution/github-pubkeys/master/github_keys.py
    --2013-09-13 16:43:02--  https://raw.github.com/illumin-us-r3v0lution/github-pubkeys/master/github_keys.py
    Resolving raw.github.com (raw.github.com)... 199.27.74.133
    Connecting to raw.github.com (raw.github.com)|199.27.74.133|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 6976 (6.8K) [text/plain]
    Saving to: `github_keys.py'
    
    100%[====================================================================================================================================================>] 6,976       --.-K/s   in 0s      

    2013-09-13 16:43:02 (81.0 MB/s) - `github_keys.py' saved [6976/6976]

* Go to the ![Applications page in your Github account settings](https://github.com/settings/applications), select `Create New Token` under `Personal Access Tokens`. Save the token you create here, you will only see it once.
* Run the helper script to test and confirm you have access to the API:
    
    root@oms:~# python ./github_keys.py -u illumin-us-r3v0lution -t 0d9b05f4a4b6d5cd4cfe43f47290b25ae3c3b06c --test
    
  You should see your github account details as a JSON HTTP response. If you fail authentication, double check your username and the token retrieved from the Github WebUI.
* Rerun the script with `-c -f /root/.ssh/id_rsa.pub` to add the pub key to your github account

If you create a key in error and wish to delete it, run the script with `--list` to obtain the ID of the SSH Key to delete, and again with `--delete <id>` to then remove the key.

