# PubSub Service

This project implements a simple Publish-Subscribe (PubSub) service using Django and Django Rest Framework.

## Build Files

The project includes the following key files:

- `.envrc`: Wrapper that leverages [`direnv`](https://direnv.net/) to manage the project's environment.
- `requirements.txt`: Lists the project dependencies (It may looks too many, but they are just Django, DRF, and drf-yasg).
- `pubsubservice`: Django project base directory.
- `topics/models.py`: Defines the Django models for Topic, Subscription, and Message.
- `topics/serializers.py`: Contains serializers for the models.
- `topics/views.py`: Implements views for creating topics, publishing messages, subscribing/unsubscribing to topics.
- `topics/urls.py`: Defines URL patterns for the API endpoints.
- `topics/test_models.py`: Includes tests for the DB Models.
- `topics/test_serializers.py`: Includes tests for the serializers.
- `topics/test_views.py`: Contains tests for the views using Django Rest Framework's `APITestCase`.

## How to Run

To run the project locally, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone git@github.com:muktarsayedsaleh/PubSubService.git
   cd PubSubService
   ```
2. **Install Dependencies:**
   Make sure [direnv](https://direnv.net/) is installed properly in your machine, and then run

   ```bash
   direnv allow
   ```

   Which will install all the dependencies and prepare the virtual environment.

   > Note: If you prefer handling your environment manually, then make sure to run the following command in your active virtual environment:
   >

   ```bash
   pip install -r requirements.txt

3. **Run Migrations:**

   ```bash
   python manage.py migrate
   ```

4. **Run the Development Server:**

   ```bash
   python manage.py runserver
   ```

   The development server will be accessible at `http://localhost:8000/`.

## How to Test

To run tests, use the following command:

```bash
python manage.py test
```

## Design Documentation

### Design Choices

- **Django**: Chosen for its robustness and built-in features for web development.
- **Django Rest Framework (DRF)**: Used for building RESTful APIs in a clean and efficient way.
- **Swagger UI with drf-yasg**: Provides a user-friendly interface for exploring and testing APIs.

### Limitations

- **Synchronous Message Sending**: The message sending to subscribers is done synchronously for simplicity. For production, consider implementing an asynchronous solution (e.g., using Celery) for scalability.
- **Error Handling**: Basic error handling is implemented. In a production environment, you may want to improve error handling, logging, and implement retry mechanisms.
- **Security**: The code assumes a trusted environment. In a real-world scenario, implement proper security measures, such as user authentication and authorization, input validation, and secure communication.

## Contribution Guidelines

1. Fork the repository and create a new branch for your feature or bug fix.
2. Commit your changes and submit a pull request.
3. Follow the project's coding style and include appropriate tests for your changes.

Feel free to reach out to the project maintainers or open an issue for any questions or concerns. Happy coding!