# Project README - Simple Brainteaser APIS

-The project is about development of APIS to power a QUIZ APP. This can be applied in scenarion when someone can choose to test his/her retention rates of different concepts they have learnt. The project also provides the expected answer to help in mastery of the concepts.

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/api/v1.0`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
	"message": "Not Found",
	"success": false
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 500: internal Serval Error

### Endpoints

#### GET /questions

- General:
  - Returns a list of question objects, success value, and total number of questions
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://localhost:5000/api/v1.0/questions`

```
{
	"categories": {
		"1": "Science",
		"2": "Art",
		"3": "Geography",
		"4": "History",
		"5": "Entertainment",
		"6": "Sports"
	},
	"currentCategory": null,
	"questions": [
		{
			"answer": "Maya Angelou",
			"category": 4,
			"difficulty": 2,
			"id": 5,
			"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
		},
		{
			"answer": "Muhammad Ali",
			"category": 4,
			"difficulty": 1,
			"id": 9,
			"question": "What boxer's original name is Cassius Clay?"
		},
		{
			"answer": "Apollo 13",
			"category": 5,
			"difficulty": 4,
			"id": 2,
			"question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
		}
	],
	"success": true,
	"totalQuestions": 22
}
```

#### POST /questions

- General:
  - Creates a new question using the submitted answer, category, difficulty and question. Returns the created question and success value.
- `curl http://127.0.0.1:5000/api/v1.0/questions -X POST -H "Content-Type: application/json" -d '{ "answer": "Barrack Obama", "category": 3, "difficulty": 1, "question": "Who was the president of US in 2015?" }' `

```
Response is


{
	"created": {
		"answer": "Barrack Obama",
		"category": 3,
		"difficulty": 1,
		"id": 29,
		"question": "Who was the president of US in 2015?"
	},
	"success": true
}
```

#### DELETE /questions/{questionid}

- General:
  - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value and deleted question.
- `curl -X DELETE http://localhost:5000/api/v1.0/questions/{questionid}`

```
{
	"deleted": {
		"answer": "Eliud Kipchoge",
		"category": 1,
		"difficulty": 1,
		"id": 26,
		"question": "Who won the marathon race in 2018"
	},
	"success": true
}
```

#### POST /questions/search

- General:
  - The api if provided with a serchterm it dispalys questions with the substring similar to searchterm otherwise is no match it displays 404 error.
  - If no search term is provided all the questions are displayed.
- `curl http://127.0.0.1:5000/api/v1.0/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "m"}'`

```
{
  "id": 15,
  "success": true
}
```

#### POST /quizzes

- General:

  - Creates a quiz using the submitted previous_questions, quiz_category, type and id. Returns the generated quiz question.

- `curl http://127.0.0.1:5000/api/v1.0/quizzes -X POST -H "Content-Type: application/json" -d '{ "previous_questions": [], "quiz_category": { "type": "History", "id": "6" } }' `

```
Response is


{
	"answer": "Brazil",
	"category": 6,
	"difficulty": 3,
	"id": 10,
	"question": "Which is the only team to play in every soccer World Cup tournament?"
}

```
