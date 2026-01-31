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

  # 3. LATEST UPDATES
  - block: markdown
    id: news
    content:
      title: Latest Updates
      text: |
        * **Dec 2025:** Attended **Anton Paar XRD Workshop** (XRDynamic 500) on total scattering and PDF analysis. [[Read Learning Report]](#)
        * **Sep 2025:** Selected participant for the **1st National Neutron Scattering School** at [Oak Ridge National Laboratory (ORNL)](https://www.ornl.gov/). [[View Agenda]](uploads/nns_agenda.pdf)
        * **Aug 2025:** Presented *Adhesives for Personalized Wearable Devices* at **[ACS Fall 2025](https://www.acs.org/)** (Washington, D.C.).
        * **June 2025:** Attended **Anton Paar Rheo-Polarized Imaging Workshop** with Photron high-speed camera integration. [[Read Learning Report]](#)
        * **Sep 2024:** **[FUNDED]** Drafted successful **$30,000 Commonwealth Cyber Initiative** grant for thermochromic textile research. [[Read Project Details]]({{< relref "project/adhesion-analysis" >}})
    design:
      columns: '2'

  # 4. SELECTED PROJECTS
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

  # 6. ACADEMIC RESEARCH (Block 1)
  - block: experience
    id: experience
    content:
      title: Academic Research
      items:
        - title: Graduate Research Assistant
          company: VCU Soft Functional Materials Lab
          company_url: 'https://vcusoftmaterialslab.weebly.com/'
          location: Richmond, VA
          date_start: '2024-09-01'
          date_end: ''
          description: |2-
            * **Grant Success:** Drafted successful **$30,000 grant proposal** (Commonwealth Cyber Initiative) for thermochromic socks.
            * **Metrology:** Engineered an **Integrated Optical Metrology System** (Python/OpenCV) increasing throughput by >300%.
            * **Award:** Recieved Graduate Assistantship (Full Tuition Waiver).
    design:
      columns: '2'

  # 7. INDUSTRY EXPERIENCE (Block 2)
  - block: experience
    content:
      title: Industry Experience
      items:
        - title: Technical Project Manager
          company: Kreative Organics Pvt. Ltd.
          company_url: 'https://kreativeorganics.com/'
          location: Hyderabad, India
          date_start: '2023-05-01'
          date_end: '2024-05-01'
          description: |2-
            *Recruited via Deep Thought Edutech.*
            * **Mentors:** [Mr. Ravi Seelamsetty (CEO)](https://www.linkedin.com/in/raviseelamsetty/) & [Tarun Ayitham](https://www.linkedin.com/in/tarunayitham/).
            * Directed **CAPA/Root Cause Analysis** initiatives ensuring FDA audit readiness.
            * Executed **SAP System Requalification** with precision cutover.

        - title: Technical Intern
          company: Deep Thought Edutech
          company_url: 'https://deepthought.education/'
          location: Remote
          date_start: '2022-04-01'
          date_end: '2022-10-01'
          description: |2-
            * Developed logic frameworks and documentation standards.
            * Contributed to educational technology logic frameworks.

        - title: Technical Project Intern
          company: Kreative Organics Pvt. Ltd.
          company_url: 'https://kreativeorganics.com/'
          location: Hyderabad, India
          date_start: '2022-10-01'
          date_end: '2023-04-01'
          description: |2-
            * Engineered **Supply Chain Optimization Workflow** reducing research time by **70%**.
            * Designed **Standardized Chemical Data Protocol** (Python/Docker) with **90%** accuracy improvement.
    design:
      columns: '2'

  # 8. SKILLS
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

  # 9. CONTACT
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
