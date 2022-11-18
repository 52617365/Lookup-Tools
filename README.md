# Lookup-Tools

## Lookup-Tools is an automated parsing project that uses pandas made to assist with my main project Lookup.

<details>
<summary>What problems is this project trying to solve?</summary>

- Lookup uses MongoDB to store data, the data has to be parsed, and preferably (not mandatory), in JSON format before it
  can be stored
  there.
- Parsing the data is a very time-consuming task, and it is not very time-efficient to do it all manually.
- Lookup-Tools is a project that will help me with the act of parsing data and adding additional data related to the
  dataset *automagically*, leaving me with less manual work to achieve
  my end goal.

</details>

<details>
<summary>Why JSON?</summary>

> You are able to mongoimport data in a .csv format, why would you turn it into JSON first?

- **TLDR;** I can't guarantee the format of the file and converting it to JSON will minimize data loss.

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

- Each handled file has an encrypted SHA256 hash representation, stored in a file.
- When a file is read, it is encrypted into a SHA256 hash, and compared to the hashes stored in the file to see if it
  has already been handled.

</details>
