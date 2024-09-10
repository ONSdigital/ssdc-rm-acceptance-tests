@UI
Feature: testing the cookie selection functionality of RH UI

    Scenario: The cookies banner is displayed
        When the UAC entry page is displayed
        Then the cookies banner is displayed

    Scenario: The 'cookies' hyperlink on the cookies banner points to the cookies page
        Given the UAC entry page is displayed
        And the cookies banner is displayed
        Then the 'cookies' hyperlink on the cookies banner points to en/cookies/

    Scenario: The "View cookies" hyperlink on the cookies banner points to the cookies page
        Given the UAC entry page is displayed
        And the cookies banner is displayed
        Then the 'View cookies' hyperlink points to en/cookies/

    Scenario: The "change cookie preferneces" hyperlink points to the cookies page
        Given the UAC entry page is displayed
        And the cookies banner is displayed
        When the user accepts the cookies on the cookies banner
        Then the "change cookie preferences" hyperlink text points to en/cookies/

    Scenario: Accepting the cookies via the cookies banner is reflected in page cookies
        Given the UAC entry page is displayed
        And the cookies banner is displayed
        When the user accepts the cookies on the cookies banner
        Then all optional cookies are set to On
        
    Scenario: Rejecting the cookies via the cookies banner is reflected in page cookies
        Given the UAC entry page is displayed
        And the cookies banner is displayed
        When the user rejects the cookies on the cookies banner
        Then all optional cookies are set to Off
    
    Scenario Outline: Changing cookie selection on cookies page is reflected in the cookies
        Given the cookies page is displayed
        And the cookies banner is displayed
        And the user accepts the cookies on the cookies banner
        When the user sets the selection under <para_title> to <cookie_selection>
        Then the field <cookie_key> within the ons_cookie_policy cookie is set to <cookie_selection>
    
       Examples:
        | para_title                                | cookie_key        | cookie_selection |
        | Cookies that measure website use          | usage             | Off              |
        | Cookies that help with our communications | campaigns         | Off              |
        | Cookies that remember your settings       | settings          | Off              |


    