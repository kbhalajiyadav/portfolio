---
title: ''
date: 2025-01-31
type: landing

profile: true
toc: true

sections:
  # ===== HERO SECTION =====
  - block: hero
    content:
      title: Bhalaji Y. Kantepalle
      image:
        filename: avatar.png
      cta:
        label: 'Download CV'
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
        gradient_end: '#1565c0'
        gradient_start: '#0d47a1'
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

    # 3. LATEST UPDATES (Workshops, News, Awards)
  - block: markdown
    id: news
    content:
      title: Latest Updates
      text: |
        * **Dec 2025:** **[FUNDED]** Drafted successful **$30,000 Commonwealth Cyber Initiative** grant for thermochromic textile research. [[Read Project Details]]({{< relref "project/adhesion-analysis" >}})
        * **Dec 2025:** Attended **Anton Paar XRD Workshop** (XRDynamic 500) on total scattering and PDF analysis. [[Read Learning Report]](#)
        * **Sep 2025:** Selected participant for the **1st National Neutron Scattering School** at [Oak Ridge National Laboratory (ORNL)](https://www.ornl.gov/). [[Know more]]([uploads/nns_agenda.pdf](https://neutrons.ornl.gov/nns/2025))
        * **Aug 2025:** Presented *Adhesives for Personalized Wearable Devices* at **[ACS Fall 2025](https://acs.digitellinc.com/live/35/session/565233)** (Washington, D.C.).
        * **June 2025:** Attended **Anton Paar Rheo-Polarized Imaging Workshop** with Photron high-speed camera integration. [[Read Learning Report]](#)
    design:
      columns: '2'
  # ===== PROJECTS SECTION =====
  - block: portfolio
    id: projects
    content:
      title: Selected Projects
      filters:
        folders:
          - project
      buttons:
        - name: Academic Research
          tag: Academic Research
        - name: Industry
          tag: Industry
    design:
      columns: '1'
      view: compact
      flip_alt_rows: false

  # ===== PUBLICATIONS SECTION =====
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
      title: Experience
      items:
        - title: Graduate Research Assistant
          company: VCU Soft Functional Materials Lab
          company_url: 'https://vcusoftmaterialslab.weebly.com/'
          location: Richmond, VA
          date_start: '2024-09-01'
          date_end: ''
          description: |2-
            *Advisor:* [Dr. Christina Tang, Associate Professor](https://egr.vcu.edu/directory/christina.tang/)
            * **Grant Success:** Drafted successful **$30,000 grant proposal** (Commonwealth Cyber Initiative) for thermochromic socks.
            * **Metrology:** Engineered an **Integrated Optical Metrology System** (Python/OpenCV) increasing throughput by >300%.
            * **Award:** Recieved Fall 2025 Graduate Assistantship (Full Tuition Waiver & stipend).

        - title: Technical Project Manager
          company: Kreative Organics Pvt. Ltd.
          company_url: 'https://kreativeorganics.com/'
          location: Hyderabad, India
          date_start: '2023-05-01'
          date_end: '2024-05-15'
          description: |2-
            *Mentor:* [Mr. Ravi Seelamsetty (MD & CEO)](https://www.linkedin.com/in/raviseelamsetty/).
            * **Promoted from Intern to Manager** in 6 months for demonstrating high adaptability
            * Spearheaded **CAPA/Root Cause Analysis** initiatives ensuring FDA audit readiness.
            * Executed **SAP System Requalification** with 5-hour precision cutover

        - title: Technical Project Intern
          company: Kreative Organics Pvt. Ltd.
          company_url: 'https://kreativeorganics.com/'
          location: Hyderabad, India
          date_start: '2022-10-01'
          date_end: '2023-04-01'
          description: |2-
            *Recruited and groomed by Deep Thought Edutech.*
    - *Mentor:* [Mr. Tarun Ayitham (Founder & CEO)](https://www.linkedin.com/in/tarunayitham/).
            * Engineered **Supply Chain Optimization Workflow** reducing research time by **70%**.
            * Designed and Containerized **Standardized Chemical Data Protocol** (Python/Docker) with **90%** accuracy improvement.
            * Created **Stage-Gate Project Management Framework** which was subsequently adopted company-wide to streamline R&D timelines.
    design:
      columns: '2'
    
  # ===== SKILLS SECTION =====
  - block: features
    id: skills
    content:
      title: Technical Skills
      items:
        - name: Experimental Mechanics
          description: NMR, FT-NIR, Abbe refractometry, UV-Vis, Tensile Testing, T-Peel (ASTM D2724), Rheology, Microscopy
          icon: microscope
          icon_pack: fas
        - name: Computational & Data
          description: Python (Numpy, Pandas, OpenCV, SciPy), Metrology Throughput Optimization and anaylysis
          icon: code
          icon_pack: fas
        - name: Quality & Regulatory
          description: FDA Compliance, cGMP, CAPA, Technical writing, SOP Development, Design of Experiments
          icon: clipboard-check
          icon_pack: fas
    design:
      columns: '3'

  # ===== CONTACT SECTION =====
  - block: contact
    id: contact
    content:
      title: Contact
      email: kbhalajiyadav22@gmail.com
      
      address:
        street: 401 W Main St
        city: Richmond
        region: VA
        postcode: '23284'
        country: United States
        country_code: US
      coordinates:
        latitude: '37.5465'
        longitude: '-77.4530'
      directions: VCU College of Engineering
      autolink: true
    design:
      columns: '2'
---
