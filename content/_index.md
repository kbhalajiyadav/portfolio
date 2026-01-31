# 5. PROJECTS
  - block: portfolio
    id: projects
    content:
      title: Selected Projects
      filters:
        folders:
          - project
      buttons:
        - name: All
          tag: '*'
    design:
      columns: '1'
      view: compact   # <--- THIS IS THE FIX (was 'showcase')
      flip_alt_rows: false
