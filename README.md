# Lookup-Tools

## Lookup-Tools is an automated parsing project that uses pandas made to assist with my main project Lookup.
TODO: this README.md is currently outdated, I haven't had time to update it yet, most of the stuff on it is correct though. (20.12.2022)
<details>
<summary>What is my end goal?</summary>

- Have a search engine that can search through ~1TB of data in milliseconds.
- Each search result from the search engine should know the dataset it belongs to and the date of the dataset it belongs
  to.
- Have a catalog with all the datasets and additional related information, notably; the name of the dataset, the date of
  the dataset, and the
  number of rows in the dataset.

</details>

<details>
<summary>How will I achieve this goal?</summary>

- I will use MongoDB to store the data and I will be creating indexes on the fields that can be searched.
- I have to parse tons of data, this is where Lookup-Tools comes in to automate a lot of it.

</details>

<details>
<summary>What problems is this project trying to solve?</summary>

- Lookup uses MongoDB to store data, the data has to be parsed, and preferably (not mandatory), in JSON format before it
  can be stored
  there.
- Parsing the data is a very time-consuming task, and it is not very time-efficient to do it all manually.

</details>

<details>
<summary>What does Lookup-Tools do?</summary>

Lookup-Tools is a project that will help me with the act of parsing data by automating the process and minimizing the
manual labor needed.

It will:

- Parse data from a delimited file format with one of the following delimiters `:;.,\\s+|__`.
- The pandas python engine supports getting the dynamic delimiters from the file, but it is not very reliable, so I have
  to
  manually specify the
  delimiter. For example, it could not handle a file with a delimiter of `|` (the pipe character).
- Capture the dataset name from the file name, store it within the dataset.
- Use the dataset name to find additional information about the dataset, such as the date of the dataset, if found,
  store it within the dataset.
- It will convert the dataset into a *.json format and import it into MongoDB.
- Finally, it will analyze the dataset for additional information, such as the number of rows in the dataset and import
  it into a separate collection in MongoDB.

</details>

<details>
<summary>Why JSON?</summary>

> You are able to mongoimport data in a .csv format, why would you turn it into JSON first?

- **TLDR;** I can't guarantee the format of the file and converting it to JSON will minimize data loss, on top of this,
  to avoid the extra step of having to use mongoimport, the importing of JSON strings into MongoDB is automated by this
  tool.

For example, if you have a csv dataset that contains the following data:

```csv
id,username     ,age
1 ,John         ,Carmack,20
2 ,Jonathan.blow,21
```

Oopsies! John Carmack accidentally typed `,` instead of `.`. This will cause the data to be parsed incorrectly.
Sure, if the data was stored in a csv format with quotes this could be avoided, but we can't guarantee this.

```csv
"id","username"     ,"age"
1   ,"John, Carmack",20
2   ,Jonathan.blow  ,21
```

Example of a JSON string representation:

```json
[
  {
    "id": 1,
    "username": "John, Carmack",
    "age": 20
  },
  {
    "id": 2,
    "username": "Jonathan.blow",
    "age": 21
  }
]
```

</details>

<details>
<summary>What additional data?</summary>

- The data that is parsed is not always enough to be useful, for example, if you have a dataset with phone numbers, you
  might want to know how old the phone number is to see if it's still used.
- The additional data matcher looks at the existing dataset, and tries to find additional data related to the dataset.
  For example, if you have a dataset with phone numbers, it will try to find the breach date of the dataset containing
  phone numbers,
  and add it to
  the existing dataset containing phone numbers.

#### Example of additional data

```csv
database      ,entries ,dumped
000webhost.com,15271696,2017-03-29
007.no        ,4284    ,2018-10-24
0secdb        ,384643  ,2017-03-31
1000cv.it     ,2699    ,2018-10-24
```

#### Example end result

```json
[
  {
    "id": 1,
    "username": "John, Carmack",
    "age": 20,
    "database": "000webhost.com",
    "dumped": "2017-03-29"
  },
  {
    "id": 2,
    "username": "Jonathan.blow",
    "age": 21,
    "database": "007.no",
    "dumped": "2018-10-24"
  }
]
```

</details>

<details>

<summary>How do you avoid duplicate data?</summary>

- Each handled file has an encrypted blake2b hash generated from the file contents, stored in a MongoDB collection.
- When a file is read, it is encrypted into a blake2b hash, and compared to the hashes stored in the collection to
  see if it
  has already been handled.

</details>
