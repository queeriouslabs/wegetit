# wegetit

An implementation of WeGetIt from Karl Schroeder's short story Degrees of Freedom

## terminology

For lack of better terms, "definitions" describes the term-definition-paraphrase portions of WeGetIt, while "conversations" describes the broad collection of definitions.

### possible terminology improvement

"conversation" might be a bit ambiguous so perhaps "topic" is better?

"term/definition" might lead people to feel ownership over a term, so it might
better to use something like "perspective" or "interpretation"?

## page/flow - single-page version

- The Page
  - Overview/description of WeGetIt
  - List of convos
    - - for new convo
    - Entry
      - UUID anchor
      - Title
      - Description
      - List of definitions
        - - for new definition
        - Entry
          - UUID anchor
          - Term + UUID indicating which initial definition of the term
          - Initial definition
          - List of Paraphrases
            - - for new paraphrase
            - Entry
              - UUID anchor
              - Yes/No judgment
              - Paraphrase

### Endpoints / API

- `GET /`
  Returns:
  HTML rendering of the main page

- `POST /threads`

  Parameters:

  - title : String
  - description : String

  Returns:

  - Redirect to the mainpage with an anchor to #ThreadID for a newly
    created thread

- `POST /threads/:convo_id/perspectives`

  Parameters:

  - term : String
  - initial_interpretation : String

  Returns:

  - Redirect to the mainpage with an anchor to #PerspectiveID for the newly
    created perspective

- `POST /threads/:convo_id/perspectives/:perspective_id/paraphrases`

  Parameters:

  - paraphrase : String

  Returns:

  - Redirects to the mainpage with an anchor to #ParaphraseID for the newly
    created paraphrase

## pages/flows - minimal version

- Main Page
  - Overview/description of WeGetIt
  - List of conversations
- Create Convo
  - Title + Description
- View Convo
  - Title + Description
  - List of definitions in this conversation --click--> view definition
- View Definition
  - Term
  - Initial definition
  - Add your own paraphrase
  - Other paraphrases + good/bad judgment

## pages/flows - fuller version?

- Main Page
  - Overview/description of WeGetIt
  - List of conversations you've created
  - List of conversations you've joined
- My Conversations Page
  - Convo ID + Description --click--> Manager for this convo
  - Create New Convo button
- Manage Convo
  - Overview of what the conversation is about
  - List of definitions in this conversation --click--> view definition
- View Definition
  - Term
  - Initial definition
  - Paraphrases + good/bad judgment

## considerations

- ease of setup - no signup required
- privacy/anonymity
- ability to return to conversations/connect up multiple convos?
- how to have more feedback beyond just "we get it!", without it devolving into arguments?
  - idea: maybe let the definer highlight some parts of the definition and explicitly mark those as not what they mean?
