---
# Leave the homepage title empty to use the site title
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
        
        My work focuses on the fracture mechanics of soft interfaces—specifically avoiding the "False Positive" trap in wearable adhesion. I leverage Python (Pandas, OpenCV) to automate mechanical data analysis, turning raw peel tests into actionable fracture energy insights.
    design:
      columns: '2'

  # 3. RECENT NEWS
  - block: markdown
    id: news
    content:
      title: Recent News
      text: |
        * **[Sep 2025]** Selected participant for the **1st National Neutron Scattering School** at [ORNL](https://www.ornl.gov/).
        * **[Aug 2025]** Presented *Adhesives for Personalized Wearable Devices* at **[ACS Fall 2025](https://www.acs.org/)** (Washington, D.C.).
        * **[May 2025]** Attended **Anton Paar Rheology Workshop** on soft matter characterization.
        * **[Sep 2024]** Secured **$30,000 Commonwealth Cyber Initiative** grant for thermochromic textile research. [Read project details]({{< relref "project/adhesion-analysis" >}}).
        
        [**View Archived News →**](#)
    design:
      columns: '2'

  # 4. SELECTED PROJECTS (View: Compact)
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
      view: compact
      flip_alt_rows: false

  # 5. PUBLICATIONS
  - block: collection
    id: publications
    content:
      title: Publications
      filters:
        folders:
          - publication
    design:
      columns: '2'
      view: citation

  # 6. EXPERIENCE
  - block: experience
    id: experience
    content:
      title: Experience
      items:
        - title: Graduate Research Assistant
          company: VCU Soft Functional Materials Lab
          company_url: 'https://vcusoftmaterialslab.weebly.com/'
          location: Richmond, VA
          date_start: '2024-09-01'
          date_end: ''
          description: |2-
            * Drafted successful **$30,000 grant proposal** (Commonwealth Cyber Initiative).
            * Engineered an **Integrated Optical Metrology System** (Python/OpenCV).

        - title: Technical Project Manager
          company: Kreative Organics Pvt. Ltd.
          company_url: 'https://kreativeorganics.com/'
          location: Hyderabad, India
          date_start: '2023-05-01'
          date_end: '2024-05-01'
          description: |2-
            * Directed **CAPA/Root Cause Analysis** initiatives ensuring FDA audit readiness.
            * Executed **SAP System Requalification**.

        - title: Technical Intern
          company: Deep Thought Edutech
          company_url: 'https://deepthought.education/'
          location: Remote
          date_start: '2022-04-01'
          date_end: '2022-10-01'
          description: |2-
            * Developed logic frameworks and documentation standards.
    design:
      columns: '2'

  # 7. SKILLS
  - block: features
    id: skills
    content:
      title: Technical Skills
      items:
        - name: Experimental Mechanics
          description: Universal Testing (Instron), T-Peel (ASTM D2724), Rheology, Microscopy.
          icon: microscope
          icon_pack: fas
        
        - name: Computational & Data
          description: Python (Pandas, OpenCV, SciPy), MATLAB, Automated Pipelines.
          icon: code
          icon_pack: fas
          
        - name: Quality & Regulatory
          description: FDA Compliance, cGMP, CAPA, DoE.
          icon: clipboard-check
          icon_pack: fas
    design:
      columns: '1'
      view: 3

  # 8. CONTACT
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
