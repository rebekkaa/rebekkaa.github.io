---
# Leave the homepage title empty to use the site title
title: ""
date: 2022-10-24
type: landing
title: Rebekka Wohlrab's personal website

design:
  # Default section spacing
  spacing: "6rem"

sections:
  - block: about_cust.biography
    id: about
    content:
      title: About me
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: admin
  - block: markdown
    id: news
    content:
      title: Recent news
      subtitle: "[All news>>](/news)"
      text: |-
        {{< readfromfile "/content/newslist.dat" 5 >}}
    design:
      columns: '2'
      spacing:
        padding: 30px 0 30px 0;
  - block: people
    content:
      title: Meet the Team
      subtitle: ""
      # Choose which groups/teams of users to display.
      #   Edit `user_groups` in each user's profile to add them to one or more of these groups.
      user_groups:
          - PhD Students
          - Postdocs
          - Administration
          - Researchers
          - Visitors
          - Alumni
      sort_by: Params.user_groups
      sort_ascending: true
    design:
      show_interests: true
      show_role: true
      show_social: false
      columns: '2'
---