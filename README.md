# collection-of-projects

## Description
Это репозиторий для размещения небольших проектов.


```sh
export repo=text-editor

git remote add $repo ../a/$repo
git fetch $repo
git subtree add --prefix=$repo/ $repo main --squash
git subtree add --prefix=$repo/ $repo main
git push origin main

```
