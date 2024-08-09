# Interpol Red DL


`Interpol Red-DL` is a project designed to retrieve, save and display data published by [Interpol on wanted persons](https://www.interpol.int/How-we-work/Notices/Red-Notices/). It primarily consists of three Dockerized services: `api-poller`, `notice-saver` and `notice-dashboard`.  
- `api-poller` periodically retrieves [Red Notices](https://www.interpol.int/How-we-work/Notices/Red-Notices/View-Red-Notices) from the Interpol API and sends it to RabbitMQ queue.  
- `notice-saver` reads notices from the queue, and optionally downloads the relevant images and classifies the arrest warrants by offense types before saving the information into the database. 
- `notice-dashboard` offers an interactive dashboard built with Streamlit for viewing relevant statistics, as well as accessing the notice list and detailed information.

## System Overview
![High-Level Docker Diagram](https://github.com/user-attachments/assets/5c57a0a5-8c63-4e75-98be-88cece9d1b5d)

## Usage

### Prerequisites
Ensure that Docker Engine is installed on your system.

### Running Interpol-Red-DL
To build and start the dockerized applications in detached mode, use the command:
```bash
docker-compose up --build -d
```
The dashboard runs on `http://localhost:5000` by default.
### Stopping Interpol-Red-DL
To stop the application and remove the containers, use the command:
```bash
docker-compose down
```
### Testing
To run the tests, use the commands:
```bash
# Run tests for api_poller:
docker-compose run api_poller pytest

# Run tests for notice_server
docker-compose run notice_server pytest
```
## App-Level Configuration Options
#### api-poller/.env
| Name                    | Description                                                |
| ----------------------- | ---------------------------------------------------------- |
| `RED_LIST_URL`          | URL to Red List API endpoint                           |
| `API_RATE_LIMIT_DELAY`  | Delay in seconds between each fetched notice           |
| `POLL_INTERVAL`         | Delay in seconds between each run of polling           |
| `QUERY_STRATEGY`        | Strategy to be used to query notice lists <br>`0`: `Simple Default Search`, `1`: `Minimal Brute-force Search` |

#### notice-dashboard/.env
| Name                          | Description                                              |
| ----------------------------- | ---------------------------------------------------------|
| `SERVE_DOWNLOADED_IMAGES`        | `0`: Display notice-related images directly from Interpol server <br>`1`: Serve notice-related images as downloaded by `notice-saver`  |


## Additional Notes
### HTTP Request Header Spoofing
Although the Interpol API is publicly available, it appears to be intended for internal use only, with measures to prevent bots.  
The Interpol API includes User-Agent and other header field validation checks to prevent bots. Therefore `api-poller/config-data/headers.json` and ``notice-saver/config-data/headers.json`` files are provided to spoof headers.


### Querying Strategy
Interpol displays up to 160 notices per search result, advising users to refine search criteria to locate specific notices. However there are approximately 7000 notices in circulation at the time of this project's writing. Additionally, it has been observed that the notices on the default page are sorted by upload date in descending order, ensuring that the 160 recent notices are always displayed first.
To address this issue querying strategies have been developed which implements `Strategy` interface and has `get_query_options_list` method that returns list of set of search filters to be used for queries:
- `SimpleDefaultSearch`: This can be ran as a background worker to fetch notices from the default page ensuring the database is always up to date.
- `BruteforceSearch`: This provides a detailed yet customizable search strategy where the results are brute-forces by using any of the selected filters from: arrest warrant issuing country, age, nationality, gender and name in that order.
- `CompositeStrategy`: This allows for combining multiple strategies together   

The above classes offer a flexible approach to easily adapt to changes in notice counts on the Interpol server. Additionally a warning message is logged if the notice count of the given query response reaches the imposed limit so the changes to the strategy could be made.

The above classes can be utilized to develop an efficient brute-force strategy, `minimal_bruteforce_search`  as defined within the `QueryStrategyFactory` class, where a broader search is applied to regular countries (less filters applied), while a more targeted search is conducted for countries exceeding the imposed limit.  
This strategy could be ran once and then `SimpleDefaultSearch` could be used to poll the latest notices at fixed intervals.

In my tests, it took 1.12 hours to retrieve 15,714 notices, including duplicates. In total, I successfully retrieved 6,725 out of 6,743 notices at the time of writing. The missing notices are likely due to undefined nationality and age, which prevented them from being filtered down.

### Offense Type Classification
Each notice includes multiple arrest warrants, where the reason for each warrant is described as an offense/charge explanation string. Furthermore each offense explanation may include multiple offenses. These strings can sometimes be in different languages, adding complexity to the task of categorizing the arrest warrants into specific categories. To assist with this, the project provides a helper script, `scripts/data_cleaning/get_offense_strings.py`, which retrieves the offense strings and can be useful in creating distinct offense type categories.

The `OffenseTypeClassifier` is an interface with two implementations:
- `BasicOffenseTypeClassifier`: This uses a [naive word matching algorithm](https://en.wikipedia.org/wiki/String-searching_algorithm#Naive_string_search) to identify and assign predefined offense types based on their presence in the offense description string.  
However, this approach has significant limitations:  
  - It may miss synonymous offense types or translations in different languages (e.g. an offense described as "Criminal Organisation" might not be correctly assigned the predefined offense type "Terrorist Organisation").  
  - If one predefined offense type is a substring of another, both offense types may be incorrectly assigned together (e.g "Piracy" and "Conspiracy").

- `GPTOffenseTypeClassifier`: This class intends to use OpenAI's GPT model for offense type classification. However, it is currently not implemented and raises a `NotImplementedError`.

## Disclaimer
- The project is created for demonstration purposes only. Notice data may not be used for any commercial purpose, as stated in [Interpol's Disclaimer](https://www.interpol.int/How-we-work/Notices/Red-Notices/View-Red-Notices)
