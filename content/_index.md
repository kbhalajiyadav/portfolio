---
title: ''
date: 2024-01-30
type: landing

sections:
  # 1. HERO
  - block: hero
    content:
      title: |
        Bhalaji Yadav
      image:
        filename: avatar.jpg
      cta:
        label: '**Download CV**'
        url: uploads/resume.pdf
      cta_alt:
        label: Contact Me
        url: '#contact'
      text: |
        **Materials Engineer & Researcher**

        Specializing in Soft Materials, Adhesion Mechanics, and Automated Data Analysis.
        M.S. Candidate at [Virginia Commonwealth University](https://www.vcu.edu/).
    design:
      background:
        gradient_end: '#1976d2'
        gradient_start: '#004ba0'
        text_color_light: true

  # 2. BIOGRAPHY
  - block: markdown
    content:
      title: Biography
      subtitle: ''
      text: |
        I am a Chemical & Life Science Engineering researcher bridging the gap between experimental mechanics and computational analysis. Currently pursuing my M.S. at **[Virginia Commonwealth University](https://www.vcu.edu/)**, I conduct research at the **[Soft Functional Materials Lab](https://vcusoftmaterialslab.weebly.com/)** led by [Dr. Christina Tang](https://egr.vcu.edu/directory/christina.tang/).
        
        [cite_start]My work focuses on the fracture mechanics of soft interfaces—specifically avoiding the "False Positive" trap in wearable adhesion[cite: 100]. I leverage Python (Pandas, OpenCV) to automate mechanical data analysis, turning raw peel tests into actionable fracture energy insights.
    design:
      columns: '2'

  # 3. NEWS & WORKSHOPS (The "Active Researcher" Section)
  - block: markdown
    content:
      title: Recent News
      text: |
        * **Sept 2025:** Selected participant for the **1st National Neutron Scattering School** at [Oak Ridge National Laboratory (ORNL)](https://www.ornl.gov/).
        * **Aug 2025:** Presented *Adhesives for Personalized Wearable Devices* at **ACS Fall 2025** (Washington, D.C.).
        * **Workshop:** Attended **Anton Paar Rheology Workshop** on soft matter characterization.
        * **Award:** Secured **$30,000 Commonwealth Cyber Initiative** grant for thermochromic textile research.
    design:
      columns: '2'
      css_class: 'news-section'

  # 4. SKILLS
  - block: features
    id: skills
    content:
      title: Technical Expertise
      items:
        - name: Experimental Mechanics
          description: Universal Testing (Instron), T-Peel (ASTM D2724), Rheology, Soft Material Fracture.
          icon: microscope
          icon_pack: fas
        
        - name: Computational & Data
          description: Python (Pandas, OpenCV, SciPy), MATLAB, Automated Data Pipelines, Statistical Analysis (PCA).
          icon: code
          icon_pack: fas
          
        - name: Quality & Regulatory
          description: FDA Compliance, cGMP Guidelines, CAPA/Root Cause Analysis.
          icon: clipboard-check
          icon_pack: fas
    design:
      columns: '1'
      view: 3

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
      view: showcase
      flip_alt_rows: true

  # 6. PUBLICATIONS
  - block: collection
    id: publications
    content:
      title: Publications & Presentations
      filters:
        folders:
          - publication
    design:
      columns: '2'
      view: citation

  # 7. CONTACT
  - block: contact
    id: contact
    content:
      title: Contact
      email: kbhalajiyadav22@gmail.com
      address:
        street: 401 W Main St (VCU Engineering)
        city: Richmond
        region: VA
        postcode: '23284'
        country: United States
        country_code: US
    design:
      columns: '2'
---
