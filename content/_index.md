---
title: '' 
date: 2025-01-31
type: landing 

profile: true
toc: true
show_date: false
date: false

sections:
  - block: about.biography
    content:
      username: admin

# 3. LATEST UPDATES (Workshops, News, Awards)
  - block: markdown
    id: news 
    content:
      title: Latest Updates
      text: |
        * **Dec 2025:** **[FUNDED]** Drafted successful **$30,000 Commonwealth Cyber Initiative** grant for thermochromic textile research. 
        * **Dec 2025:** Attended **Anton Paar XRD Workshop** (XRDynamic 500) on total scattering and PDF analysis.
        * **Sep 2025:** Selected participant for the **1st National Neutron Scattering School** at [Oak Ridge National Laboratory (ORNL)](https://www.ornl.gov/). [[Know more]](https://neutrons.ornl.gov/nns/2025)
        * **Aug 2025:** Presented *Adhesives for Personalized Wearable Devices* at **[ACS Fall 2025](https://acs.digitellinc.com/live/35/session/565233)** (Washington, D.C.).
        * **June 2025:** Attended **Anton Paar Rheo-Polarized Imaging Workshop** with Photron high-speed camera integration.
    design:
      columns: '2'
  # ===== PROJECTS SECTION =====
  - block: portfolio
    id: projects
    content:
      title: Selected Projects
      show_date: false
      date: false
      filters:
        folders:
          - project
      sort_by: weight
      sort_ascending: true
      buttons:
        - name: All
          tag: "*"
          # This filter only shows projects with either tag
          filter: '.js-id-academic-research, .js-id-industry'
        - name: Academic Research
          tag: Academic Research
        - name: Industry
          tag: Industry
    design:
      columns: '2'
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
      sort_by: weight
      sort_ascending: true
    design:
      columns: '2'
      view: compact


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
               {{% icon name="arrow-right" pack="fas" %}} [[Read Project Details]]({{< relref "project/optical-metrology" >}})
            * **Award:** Received Fall 2025 Graduate Assistantship (Full Tuition Waiver & stipend).

        - title: Technical Project Manager
          company: Kreative Organics Pvt. Ltd.
          company_url: 'https://kreativeorganics.com/'
          location: Hyderabad, India
          date_start: '2023-05-01'
          date_end: '2024-05-15'
          description: |2-
            *Mentor:* [Mr. Ravi Seelamsetty (MD & CEO)](https://www.linkedin.com/in/raviseelamsetty/).
            * **Promoted from Intern to Manager** in 6 months for demonstrating high adaptability.
            * Spearheaded **CAPA/Root Cause Analysis** initiatives ensuring FDA audit readiness.
            * Executed **SAP System Requalification** with 5-hour precision cutover. 
              {{% icon name="arrow-right" pack="fas" %}} [[Read Project Details]]({{< relref "project/fda-project" >}})

        - title: Technical Project Intern
          company: Kreative Organics Pvt. Ltd.
          company_url: 'https://kreativeorganics.com/'
          location: Hyderabad, India
          date_start: '2022-10-01'
          date_end: '2023-04-01'
          description: |2-
            *Recruited and groomed by [Deep Thought Edutech](https://deepthought.education/).* 

            *Mentor:* [Mr. Tarun Ayitham (Founder & CEO)](https://www.linkedin.com/in/tarunayitham/).
            * Engineered **Supply Chain Optimization Workflow** reducing research time by **70%**.
            * Designed and Containerized **Standardized Chemical Data Protocol** (Python/Docker) with **90%** accuracy improvement.
              {{% icon name="arrow-right" pack="fas" %}} [[Read Project Details]]({{< relref "project/supply-chain-automation" >}}) 
            * Created **Stage-Gate Project Management Framework** which was subsequently adopted company-wide to streamline R&D timelines.
             
    design:
      columns: '2'
      view: compact
    
  # ===== SKILLS SECTION =====
  - block: features
    id: skills
    content:
      title: Technical Skills
      items:
        - name: Experimental Mechanics
          description: Rheology • T-Peel • NMR • Microscopy
          icon: microscope
          icon_pack: fas
        - name: Computational & Data
          description: Python • OpenCV • NumPy • Pandas • SciPy
          icon: code
          icon_pack: fas
        - name: Quality & Regulatory
          description: FDA • cGMP • CAPA • SOP
          icon: clipboard-check
          icon_pack: fas
    design:
      columns: '3'

  
  # ===== CONTACT SECTION =====
  - block: contact
    id: contact
    content:
      title: Contact
      text: |
        I’m always open to oppurtunities in **soft materials, adhesion mechanics, wearable interfaces**, and **materials analytics**.

      email: contact@bhalaji.com

      # Keep location high-level (cleaner + safer)
      address:
        city: Richmond
        region: VA
        country: United States
        country_code: US

      directions: VCU College of Engineering
      autolink: true
    design:
      columns: '2'

 
          


---
