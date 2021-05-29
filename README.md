- [Chirpr](#chirpr)
  - [How we help users](#how-we-help-users)
  - [Installation](#installation)
    - [Chirpr can be installed through docker...](#chirpr-can-be-installed-through-docker)
    - [Or you can use git if you're feeling a little adventurous!](#or-you-can-use-git-if-youre-feeling-a-little-adventurous)
  - [Usage](#usage)
  - [Collaboration](#collaboration)
  - [Bugs](#bugs)

# Chirpr
Chirpr is a more humane Social Media App. You can find out more about us on our [website](https://jacob-macleod.github.io/Chirpr-Social-Network/)

Chirpr is focused on serving the needs of the user, rather than fill the pockets of big corporations. It's totally free and will always be, and adds features focused on helping people manage social media in a better way.

**Please note** that the password encryption is rather rudimentary so you sign up at you own risk! We recommend that you **do not sign up** using passwords you've used for other accounts online!

**It's Partially Done** - I've completed the first version, and although I'd like to develop more features, I'll need to make time for it

## How we help users
* Chirpr is completely free, both now and in the future
* We don't show users the likes they've recieved - this reduces comparing oneself to others because you can't
* We show users the likes of posts from people they've followed - this creates a sense of community
* We don't have a trending page - you need to follow users to see their posts. This helps to combat social media addiction
* There's no ads - your attention is not being sold
* Intrusive ads don't follow you round and track you


## Installation
### Chirpr can be installed through docker...
Simply [install](https://docs.docker.com/get-docker/) docker. Once you've done that, you can run the container with `docker run -p 5000:5000 jacobmacleod/chirpr` and navigate to http://localhost:5000/.

*This is the recommended option*

### Or you can use git if you're feeling a little adventurous!
To install Chirpr using git, make sure git, python and pip are installed, then run the following commands:

**Download the dependencies**

`git clone https://github.com/jacob-macleod/Chirpr-Social-Network.git`

`pip3 install flask pymongo`

Next, you'll next to [install](https://www.mongodb.com/try/download/community) mongodb

**To run Chirpr**

Finally, you can enter the `Chirpr-Social-Network` directory, using `cd Chirpr-Social-Network` on linux, and run:

`python3 main.py`

To open Chirpr, you can go to http://localhost:5000/

*This is not the recommended option, but it is necessary for active development!*
 
## Usage
I'd like to run Chirpr on a cloud server, but I'm still looking into options and pricings

## Collaboration
If you wish to collaborate, please open an issue to let me know!

## Bugs
If you run into a bug, please [open](https://github.com/jacob-macleod/Chirpr-Social-Network/issues) an issue!
