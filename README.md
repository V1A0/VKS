<div align="center">
	<div>
		<img width="200" src=".pic/vks-200.png" alt="VKS logo" style="position: relative; float: left; width: 200px; margin-right: 40px; margin-bottom: 90px; margin-top: 13px; pointer-events: none">
	</div>
<br>

# VKS v0.2.6 ![Python:3.9](https://img.shields.io/badge/Python-3.9-green)  
Program for analysing <b>your own</b> [vk.com] data. 
<br><b>Do not track other people without their acceptation!</b>

</div><br>

# Summary
- [Features](#Features)
- [Installation](#Installation)
- [How to run](#How-to-run)
- [How to get API_TOKEN](#How-to-get-API_TOKEN)
- [Modules](#Modules)
    - [Modules settings](#Modules-settings)
        - [Onliner](#Onliner)
        - [Hidden friends](#Hidden-friends)

---

# About

### Features
- [x] 📈 Recording online activity (module.onliner)
- [x] 🙊 Hidden friends searching (module.hidden_friends)
- [x] 📑 Particularly profile data scrapping (module.onliner)
- [x] 🎯 Multiple targets support
- [x] 👪 Multiple API tokens support
- [x] 🌐 Proxy support
- [x] ⚙️ Custom modules
    - [x] Modules exceptions
    - [x] On/Off modules
    - [x] Any delay for any module
    - [x] Easy to create your own by template!
- [x] ~~🔀 Random proxy (sslproxies.org)~~ (Banhammered by VkApi)

### Coming soon
> - [ ] 📊 Live time visualizing data
> - [ ] 📑 Scrapping profile info
> - [ ] 🎱 Predicting activity

---

# Installation

1) Clone the latest stable release 
    ```shell script
    git clone https://github.com/v1a0/vks.git
    ```

2) Install development dependencies:
    ```shell script
    cd vks
    pip3 install -r requirements.txt
    ```

---

# How to run

Before running, configure necessary settings in file `settings.py`:

| Setting | Description | Example |
| :--- | :--- | :---: |
| **API_TOKENS** | list of your VK API tokens (might contain only one) | `['000fuck...rm0a1']` |
| **TARGETS_IDS** | list of targets ids (also might contain one) | `['123', '345']` |

<small>[* How to get API token read here](#How-to-get-API_TOKEN)</small>

### Optional settings:

<details><summary><h4><code>[Show / Hide]</code></h4></summary>

| Setting | Description |
| :--- | :--- |
| **MODULES** | List of using modules |
| **MODULES_EXCEPTS** | Sets which targets (ids), modules will skip |
| **PROXY** | Custom proxy settings for all requests to API |
| **MODULES_TIMEOUTS** | How often to call (some) module |
| **REQ_FREQUENCY** | How long time script will be sleep after all modules called |

</details>

### Example 

<details><summary><h4><code>[Show / Hide]</code></h4></summary>

```python
# Main settings

API_TOKENS = [
    '000fuck0fvk000i8oppkq22so2c7binpysm5lpwxlfoxcbbir7kcr2ir8g0rgbu7lv4mo0000use0tlgrm000',
]

TARGETS_IDS = [
   '123456789', '987654321', '121201',
]



# Optional settings

MODULES = [
    modules.onliner,
    modules.my_module
]

MODULES_TIMEOUTS = {
    modules.onliner: 60,            # 60 seconds
    modules.hidden_friends: 13E7,   # only once after run
    # modules.template: 0,
}

MODULES_EXCEPTS = {
    MODULES[1]: [
        TARGETS_IDS[0], 
        TARGETS_IDS[2]
    ]
}

PROXY = {
    "http": "http://123.45.6.78:4321",
    "https": "https://123.45.6.78:4321",
    "ftp": ""
}

REQ_FREQUENCY = 0.01
```
</details>

<b>And finally just run it by python3+, like this: `python3.9 main.py`.

---

# How to get API_TOKEN

Go to
`https://vk.com/editapp?act=create`

Create "Standalone app" and copy apps ID
Replace "__APPs_ID__" in the link below to your app IP
`https://oauth.vk.com/authorize?client_id=___APPs_ID___&scope=photos,audio,video,docs,notes,pages,status,offers,questions,wall,groups,email,notifications,stats,ads,offline,docs,pages,stats,notifications&response_type=token`


<details><summary><code>[ Example ]</code></summary>

`https://oauth.vk.com/authorize?client_id=1234567&scope=photos,audio,video,docs,notes,pages,status,offers,questions,wall,groups,email,notifications,stats,ads,offline,docs,pages,stats,notifications&response_type=token`

</details>
<br>


After you visit this link you'll be automatically redirected to new link
it will be looks like:

`https://oauth.vk.com/blank.html#access_token=___YOUR_API_TOKEN____&expires_in=0&user_id=1&email=durov@t.me`
__YOUR_API_TOKEN__ it is you API_TOKEN


<details><summary><code>[ Example ]</code></summary>

`https://oauth.vk.com/authorize?client_id=000fuck0vk000i8oppkq22so2c7binpyysm5lpwxl3uliibir7kcr2ir8g0rgbu7lv4mo0000use0tlgrm000&scope=photos,audio,video,docs,notes,pages,status,offers,questions,wall,groups,email,notifications,stats,ads,offline,docs,pages,stats,notifications&response_type=token`

</details>

Official instruction:
https://vk.com/dev/access_token

---

# Modules


| Module | Description | Database | Requests |
| :--- | :--- | :---: | :---: |
| Onliner | Collecting online status of users and friends online<br>Checking and updating public users data | onliner.db<br>modules_stat.db | users.get?sex,online,photo_max_orig,online_mobile | 
| Hidden friends | Searching hidden friends<br>Analysing friends of friends | hidden_friends.db<br>modules_stat.db | friends.get?user_id=id,count=val | 
| Template | Template for future modules | None | None |


## Modules settings

<details><summary><h4><code>[Show / Hide]</code></h4></summary>


### Onliner


| Setting | Description | Located | Value |
| :--- | :--- | :---: | :---: |
| MODULES_TIMEOUTS | How often run module | settings.py | 0 - 9999999<br>60 by default |

### Hidden friends


| Setting | Description | Located | Value |
| :--- | :--- | :---: | :---: |
| MODULES_TIMEOUTS | How often run module | settings.py | 13E7<br>it's mean "run only once" |
| deepness | 1 - means you searching among friends of friends<br>2 - among friends of friends and friends of friends of friends<br>And so on | modules.hidden_friends.module_settings | 0 - 4<br>2 by default|
| max_friends | Slice of friends list. How many friends API can send back | modules.hidden_friends.module_settings | 0 - 9999999<br>1000 by default  |

</details>

[vk.com]: (https://vk.com/)
