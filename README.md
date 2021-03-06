# verify-event-recorder-service
This service is part of Verify's event recording system; its purpose is to read events from a queue and write them to a
 permanent datastore.

# Development
```./build/setup.sh``` will create a virtual environment and install dependencies required to develop locally.

To run all tests and package locally you must have docker running. Once docker is running you may execute
```./pre-commit```.

Running pre-commit will start docker-compose with Postgres and our code then run tests.

# Database Schemas

The database scripts live in [verify-event-system-database-scripts](https://github.com/alphagov/verify-event-system-database-scripts).

The tests currently rely on scripts in the migrations directory of the agove repo.

## Using pre-commit hooks

If you run the `./pre-commit` script it will suggest you install `pre-commit`.
This is a handy tool that automatically generates pre-commit hooks from the
`.pre-commit-config.yaml` file in the repo.  To install it, run:

```
brew install pre-commit
pre-commit install --hook-type pre-commit
```

### Skipping pre-commit hooks

To push without running the tests, for example if you've only changed a comment, you can disable them:
`git commit --no-verify`

## Packaging the application for release
Build the zip file to pass to Lambda by running
```
./build/package.sh
```

### Binaries
Lambda ought to work by providing a zip of the source code and the python files for the dependencies.
However, some of our python libraries are not pure python. Instead they rely on some C binaries.

These C binaries are compiled for a specific OS (and version of python) and are not valid in other environments.

Therefore binaries built on our dev machines will not work on Lambda.

As a workaround, we have created all the required binaries on a linux VM, and have added them to source control. Our
package task will use these binaries in preference to any which are created on the host system.

### Environment Variables

The following environment vars are should be defined in the lambda function:

* `DB_CONNECTION_STRING` (_required_):- The connection string used to connect to the database. This should be of the format:
`host=<hostname> dbname=<databasename> user=<username>`. The connection string could also contain `port=<portnumber>` if the database is listening on a non-standard port.
* `QUEUE_URL` (_required_):- The URL to SQS queue to read events from.
* `ENCRYPTED_DATABASE_PASSWORD` (_optional_):- The password used to connect to the database, this should be KMS encrypted. If not provided the recorder
will attempt to get an IAM token to connect to the database as the user specified in `DB_CONNECTION_STRING`.

Also required is either:
* `ENCRYPTION_KEY`:- the encryption key used to decrypt messages found in the queue.
OR
* `DECRYPTION_KEY_BUCKET_NAME`:- An S3 bucket name where a file containing the decryption key for events is stored.
* `DECRYPTION_KEY_FILE_NAME`:- The file in the above containing the decryption key.
