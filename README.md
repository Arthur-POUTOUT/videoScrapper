# Description

## Instalation :
```sh
python3.8 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Utilisation :
```sh
python scrapper.py --input input.json --output output.json
```

## Input :
L'input doit être un fichier json de la forme :
```json
{
    "videos_id": [
        "fmsoym8I-3o",
        "JhWZWXvN_yo"
        //id des vidéos
    ]
}
```

## Output :
L'output est un fichier json de la forme :
```json
{
    "id_video": {
        "Title": "titre",
        "ChannelName": "nom de la chaine",
        "NumberLikes": 30401,
        "Description": "Description de la vidéo",
        "DescriptionLinks": {
            "Links": [ 
                //url http ou https
            ],
            "Timestamps": [
                // de la forme XX:XX
            ]
        },
        "Comments": [
            {
                "cid": "id_comment",
                "text": "text",
                "time": "time in string. ex: 'il y a 10 ans'",
                "author": "Bob Brown",
                "channel": "id_channel",
                "votes": "nb upvote",
                "photo": "url photo d profil",
                "heart": false,
                "reply": false,
                "time_parsed": 1353075210.117423
            }
        ]
    },
    //Prochain id de vidéo + valeur
}
```

## Test :
Lors de exécution de pytest, il ne trouve pas le module youtube_comment_downloader.

Si on comment le code concernant ce module (import, methode _getComments() et appel de la méthode),
Tous les tests ne concernant pas les commentaires passent