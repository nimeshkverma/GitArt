
#GitArt
### Python Package to Create Art though Git

Presently allows users to Create Heart Shape on their GitHub Profile Contibution Summary

![Repo Tree](https://github.com/nimeshkverma/GitArt/blob/master/images/HeartPreview.jpg)

## How To Make a Heart 
- Install the Package using the command : `pip install GitArt`
- Import the `Heart` module from `GitArt`
- Create an object of `GitHeart`
- Call the `create_heart` function of the object created with arguments `git_repo_url`, `max_commits` and `weeks_from_now`. Last two arguments are optional.

Code for above steps:-
In the Command Line:-

`pip install GitArt`

In a python script or python shell:-

```
 from GitArt import Heart
 git_heart_obj = Heart.GitHeart()
 git_repo_url = 'git@github.com:nimeshkverma/HelloWorld.git'

 #To Get Heart with default commits and with end_week as present week
 git_heart_obj.create_heart(git_repo_url=git_repo_url)

 #To Get Heart with 10 commits per day and the heart border in the week = present_week -2
 git_heart_obj.create_heart(git_repo_url=git_repo_url, max_commits=10, weeks_from_now=2)
 ```

Thanks <a href="https://github.com/locx">locx</a> for the idea :)

![Repo Tree](https://github.com/nimeshkverma/GitArt/blob/master/images/NimSubtleQuote.jpg)
