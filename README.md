# WikiScrapper

This project has been developed as part of a Web Mining course, which took place during the winter semester of 2019-2020 in Ben Gurion University.
In this repo you can find the given task and our submitted notebook.

## Supported patterns:

Cast patterns-
We support lists where the title of the list is "Cast" or "[a-zA-z]* \s cast" (i.e. "Vocal cast", "Primary cast", etc.).

Awards patterns-
We will try to collect the information from the tables in the page of the actor.
In case we couldn't find the information there we will look in the following link:
https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_firstname_lastnme where firstname and last name varies with the actor name
we will count from the tables the occurrences of won,honored,honoured and sum them to number of awards won by the actor


## Authors:
  - Nofar Turteltaub
  - Saar Guttman
