# Code Standards and Style Guide

## Format

Our base code style is [PEP8](https://www.python.org/dev/peps/pep-0008/), but we allow a max line length of 120.

Check formatting and dead code with

```shell
make lint
```

## Code Standards

### Context Use

We make use of the [Behave Context](https://behave.readthedocs.io/en/stable/tutorial.html#context) object to store data
that is needed across multiple steps of a scenario.

To prevent the context from becoming cluttered and confusing to use, we define some rules for how we interact with it:

#### Only step functions and environment hooks should interact with the context attributes

Other none step or hook functions shouldn't be passed the entire context and should certainly not modify it. Instead,
pass in explicit variables from the context and return new ones as required. Try to make all none step functions
pure/deterministic.

e.g.

```python
@step('a thing happens')
def step_to_do_a_thing(context):
    context.some_var = helper_function(context.emitted_cases[0])
```

#### Context Index

Every context attribute used by the tests must be described here. This table is parsed into the code to drive audit
logging upon failure in the [audit_trail_helper](/acceptance_tests/utilities/audit_trail_helper.py).

<div id="context-index-table">

| Attribute                          | Description                                                                    | Type     |
|------------------------------------|--------------------------------------------------------------------------------|----------|
| test_start_utc_datetime            | Stores the UTC time at the beginning of each scenario in an environment hook   | datetime |
| survey_id                          | Stores the ID of the survey generated and or used by the scenario              | UUID     |
| collex_id                          | Stores the ID of the collection exercise generated and or used by the scenario | UUID     |
| emitted_cases                      | Stores the caseUpdate DTO objects emitted on `CASE_UPDATE` events              | List     |
| emitted_uacs                       | Stores the UAC DTO objects from the emitted `UAC_UPDATE` events                | List     |
| pack_code                          | Stores the pack code used for fulfilments or action rules                      | str      |
| template                           | Stores the column template used for fulfilments or action rules                | Template |
| telephone_capture_request          | Stores the UAC and QID returned by a telephone capture API call                | Dict     |
| notify_template_id                 | Stores the ID of the sms template used for the notify service                  | UUID     |
| fulfilment_response_json           | Stores the response JSON from a `POST` to the Notify API                       | Dict     |
| phone_number                       | Stores the phone number needed to check the notify api                         | str      |
| email                              | Stores the email address needed to check the notify api                        | str      |
| message_hashes                     | Stores the hash of sent messages, for testing exception management             | List     |
| correlation_id                     | Stores the ID which connects all related events together                       | UUID     |
| originating_user                   | Stores the email of the ONS employee who originally initiated a business event | str      |
| sent_messages                      | Stores every scenario sent message for debugging errors                        | List     |
| scenario_name                      | Stores the scenario name and uses it for unique originating users in messages  | str      |
| case_id                            | Stores the case_id of a case used in the scenario                              | UUID     |
| bulk_refusals                      | Stores created bulk refusal cases we expect to see messages for                | List     |
| bulk_invalids                      | Stores the create bulk invalid cases we expect to see messages for             | List     |
| bulk_sample_update                 | Stores the create bulk sample update cases we expect to see messages for       | List     |
| bulk_sensitive_update              | Stores the bulk sensitive update cases we expect to see messages for           | List     |
| expected_collection_instrument_url | Stores the collection instrument URL expected on emitted `UAC_UPDATE` events   | str      |
| fulfilment_personalisation         | Stores the personalisation values from a received fulfilment request event     | Dict     |
| sample                             | Stores the parsed sample file rows, split into `sample` and `sensitive`        | List     |
| uacs_from_actual_export_file       | actual uacs written to file                                                    | List     |
</div>

### Sharing Code Between Steps

Step files should not import code from other step files, where code can be shared between steps they should either be in
the same file, or the shared code should be factored out into the utilities module.

### Step wording

Steps should be written in full and concise sentences, avoiding unnecessary abbreviations and shorthand. They should be
as understandable and as non-technical as possible.

### Assertions

Assertions should use the [`test_helper`](acceptance_tests/utilities/test_case_helper.py) assertion methods and should
always include a message with relevant explanation and data where it is useful.

### Step parameter types

Where we need [step parameters](https://behave.readthedocs.io/en/stable/tutorial.html#step-parameters) to include more
complex data than single strings or the other basic types supported by the default parser, we
use [custom registered types](https://behave.readthedocs.io/en/stable/api.html#behave.register_type). These are
registered in the [environment.py](acceptance_tests/features/environment.py) so they are available to all steps.

For example, our `json` type lets us write JSON data in the steps which will be parsed into python objects like so:

```python
@step('this step receives a json parameter {foo:json}')
def example(foo):
    pass
```

This example step could be called with a JSON object which will be parsed into a dictionary:

```gherkin
When this step receives a json parameter {"spam": "eggs"}
```

And our `array` type allows us to parse JSON arrays into python lists, e.g.

```python
@step('this step receives an array parameter {foo:array}')
def example(bar: List):
    pass
```

```gherkin
When this step receives an array parameter ["spam", "eggs"]
```
