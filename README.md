# Vegas Odds Getter
### Azure function fails
+ Due to a bug in [fake-useragent](https://github.com/hellysmile/fake-useragent/pull/110) the azure function currently fails
+ Cron job has been set to run once a week to track if the issue has been resolved
+ The issue is with a class name in html being updated
+ Estimated time is if the owner does not respond by roughly 09/01/2022 then the package will be moved to a fork that can be worked on