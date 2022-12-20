# gitea-extract-users

<p align="center">
  A Python script to extract the list of users of a GiTea instance, unauthenticated or authenticated.
  <br>
  <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/p0dalirius/Joomla-1.6-1.7-2.5-Privilege-Escalation-Vulnerability">
  <a href="https://twitter.com/intent/follow?screen_name=podalirius_" title="Follow"><img src="https://img.shields.io/twitter/follow/podalirius_?label=Podalirius&style=social"></a>
  <a href="https://www.youtube.com/c/Podalirius_?sub_confirmation=1" title="Subscribe"><img alt="YouTube Channel Subscribers" src="https://img.shields.io/youtube/channel/subscribers/UCF_x5O7CSfr82AfNVTKOv_A?style=social"></a>
  <br>
</p>

## Features

 - [x] Dump all users of a remote GiTea instance, unauthenticated (misconfiguration of the instance).
 - [x] Dump all users of a remote GiTea instance, authenticated using `i_like_gitea` cookie in `--cookie` option.
 - [x] Export users and emails to a JSON file, specified by option `--outfile`.

## Usage

```
$ ./gitea-extract-users.py -h
Dump GiTea users via /explore/users endpoint - v1.1 - by @podalirius_

usage: gitea-extract-users.py [-h] -t TARGET [-o OUTFILE] [-c COOKIE]

Dump GiTea users via /explore/users endpoint

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        IP address or hostname of the GiTea to target.
  -o OUTFILE, --outfile OUTFILE
                        Output JSON file of all the found users.
  -c COOKIE, --cookie COOKIE
                        i_like_gitea cookie to dump users in authenticated mode.
```

## Example output format:

```json
{
    "target": "https://git.podalirius.poc",
    "users": [
        {
            "mail": "podalirius@podalirius.poc",
            "username": "Podalirius",
            "fullname": "Podalirius Podalirius",
            "joined": "Nov 05, 1605"
        }
    ]
}
```