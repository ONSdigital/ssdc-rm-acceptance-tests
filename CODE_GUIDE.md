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

Every context attribute used by the tests should be described here.

| Attribute                 | Description                                                                     |
| ------------------------- | ------------------------------------------------------------------------------- |
| test_start_local_datetime | Stores the local time at the beginning of each scenario in an environment hook  |
| survey_id                 | Stores the ID of the survey generated and or used by the scenario               |
| collex_id                 | Stores the ID of the collection exercise generated and or used by the scenario  |
| emitted_cases             | Stores the caseUpdate DTO objects emitted on `CASE_UPDATE` events               |
| emitted_uacs              | Stores the UAC DTO objects from the emitted `UAC_UPDATE` events                 |
| pack_code                 | Stores the pack code used for fulfilments or action rules                       |
| template                  | Stores the column template used for fulfilments or action rules                 |
| telephone_capture_request | Stores the UAC and QID returned by a telephone capture API call                 |
| notify_template_id        | Stores the ID of the sms template used for the notify service                   |
| phone_number              | Stores the phone number needed to check the notify api                          |

### Sharing Code Between Steps

Step files should not import code from other step files, where code can be shared between steps they should either be in
the same file, or the shared code should be factored out into the utilities module.

### Step wording

Steps should be written in full and concise sentences, avoiding unnecessary abbreviations and shorthand. They should be
as understandable and non-technical possible.

### Assertions

Assertions should use the [`test_helper`](acceptance_tests/utilities/test_case_helper.py) assertion methods and should
always include a message with relevant explanation and data where it is useful.
