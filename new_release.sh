#!/usr/bin/env bash
set ue

cd $(dirname $0)

# Make sure that we are on the master branch, it is up to date and there are no uncommited changes.
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "master" ]; then
  echo "Release can only be done from the master branch. You are currently on $BRANCH."
  exit 1
fi
echo "Making sure that your master branch is up to date."
PULL_MESSAGE=$(git pull)
if [ "$PULL_MESSAGE" != "Already up to date." ]; then
  echo "The master branch was not up to date. Now it has been updated. Check the new updates," \
  "and if you still want to do a release then call the release script again."
  exit 1
fi
if [ -n "$(git status -s)" ]; then
  echo "There are uncommited (or unstaged) changes. For safety reasons, release is blocked in" \
    "such case."
  exit 1
fi

# Parse the current major, minor and patch version numbers.
CURRENT_VERSION=$(cut  -d\' -f2 src/texas_holdem/__version__.py)
echo "The current version is: ${CURRENT_VERSION}."

IFS='.' read -a VERSION_NUMBERS <<< $CURRENT_VERSION
MAJOR=${VERSION_NUMBERS[0]}
MINOR=${VERSION_NUMBERS[1]}
PATCH=${VERSION_NUMBERS[2]}

echo "What kind of version increment do you want to do?"
select inc_type in "Major version" "Minor version" "Patch version"; do
  case $inc_type in
    "Major version" )
        NEW_VERSION="$((MAJOR + 1)).0.0"
        break
        ;;
    "Minor version" )
        NEW_VERSION="$MAJOR.$((MINOR + 1)).0"
        break
        ;;
    "Patch version" )
        NEW_VERSION="$MAJOR.$MINOR.$((PATCH + 1))"
        break
        ;;
  esac
done

# Update CHANGELOG and __version__.py and commit changes.
sed -i "s/master/$NEW_VERSION/" CHANGELOG.rst
sed -i '5imaster\n------------------\n\n' CHANGELOG.rst
sed -i "s/$CURRENT_VERSION/$NEW_VERSION/" src/texas_holdem/__version__.py
git commit -am "Version $NEW_VERSION"

# Add tag and push it to Github
TAG="v${NEW_VERSION}"
git tag $TAG
git push tag $TAG
