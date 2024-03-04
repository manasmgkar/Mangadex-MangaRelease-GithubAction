# Mangadex-MangaRelease-GitHubAction

This Project was created since Mangadex does not have a Mobile APP nor does it have email-based notifications to allow users to track Manga Releases. For me as i was travelling for work quite a bit plus having to manually check reddit subs and also get exposed to spoilers in the process was a literal pia so i decided to create this GitHub Action to Track a certain manga that did not have a offical English Translation at that point of time since scanlation teams used to translate the managa panel by panel painstakingly re-drawing the text boxes etc(offical English Translation uploads are not allowed by mangadex) and upload the scanlation to MangaDex. This action served quite well until we started getting a official English Translation release via the publishers K manga wesbite/app. 

I thought why not open source this code as this might be useful to everyone else out there to track mangas that still do not have official English/Other translations as thousands of Mangas with international following do not have a official English/Other Translation on official release websites thus are scanlated by groups and uploaded to Mangadex. 

## How to Use this Action 
1. Fork this Repo to your account.
2. Add the Manga-id from the Mangadex api for your specific manga in the **config.cfg**
3. Fetch the Manga-id using the manga title using the mangadex api using your favourite api request tool(example postman etc)
https://github.com/EMACC99/mangadex/blob/main/README.md#searching-manga
4. Add the Manga-id and the last released chapter in the records.json file's respective fields
5. Create your secrets in Github's Settings under the Action section as shown in the screenshot below ensure your secret name is exactly in the same format
![secrets](https://github.com/manasmgkar/Mangadex-MangaRelease-GithubAction/assets/76769697/5df3b062-b994-49f5-8422-229266cae6f2)
5. Run the action and keep a eye on the bill,fine tune to your liking.

### Helpful Links to Get Those who are new to GitHub Actions started on Setting up actions
https://docs.github.com/en/actions/quickstart 

### Additonal Functionality thats disabled.
Some code has been commented out if uncommented you will receive the manga chapter in a pdf format directly on your email id,has been commented out because when creating a pdf the manga image quality is lowered and since Mangas are a visual medium image quality being lowered destroys the readability.
