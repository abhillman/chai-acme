Test that links do not show `javascript:void(0)` for citations:
  $ python -m gscholar.parser.tests.harness $HTML_PATH/chimichanga_0.html | jq '.[-1]'
  {
    "kind": "citation",
    "link": null
  }
