from typing import List
import json
import random
import string
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from samplePlan import scrape_sample_plan
from parseStudentDegree_DeepSeekop import parse_degreeworks_pdf
from pydantic import BaseModel, Field, ValidationError
from typing import List
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import re

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

truman_req = [
  {
    "Perspective": "Communication Skills Perspective",
    "Subsection": [
      {
        "Section": "Writing as Critical Thinking",
        "Courses": [
          "ENG 190 Writing as Critical Thinking, 3 Credits"
        ]
      },
      {
        "Section": "Speaking",
        "Courses": [
          "COMM 170 Public Speaking, 3 Credits",
          "COMM 252 Interpersonal Communication, 3 Credits",
          "COMM 276 Oral Advocacy & Debate, 3 Credits"
        ]
      }
    ]
  },
  {
    "Perspective": "Social Perspective",
    "Subsection": [
      {
        "Section": "Social Perspective from two prefixes or more",
        "Subsection": [
          {
            "Section": "Missouri Statute",
            "Courses": [
              "HIST 104 US History I, 1607-1877, 3 Credits",
              "HIST 105 US History II, 1877-Present, 3 Credits",
              "HIST 1104 US History I, 3 Credits",
              "HIST 1105 US History II, 3 Credits",
              "HIST 201 US History & Historiography I, 3 Credits",
              "HIST 2100 US Institutional History, 1 Credit",
              "HIST 298 American Institutional History, 1 Credit",
              "HIST 3103 WE/Historiography of the U.S., 4 Credits",
              "HIST 313 WE/US Hist/Historiography 1877, 4 Credits",
              "HIST 314 WE/Modern US Historiography, 4 Credits",
              "HIST 326 WE/History of Missouri, 4 Credits",
              "HIST 374 WE/History of American Law, 4 Credits",
              "HIST 424 WE/Nat'l Development of US, 4 Credits",
              "POL 011 MO Statute, 0 Credits",
              "POL 101 Constitutional Government, 1 Credit",
              "POL 161 American Natl Government, 3 Credits",
              "POL 262 State & Local Government, 3 Credits",
              "JUST 307 American Law & Society, 3 Credits"
            ]
          },
          {
            "Section": "Additional Social Perspective Courses",
            "Courses": [
              "ART 222 Global Art to 1400, 3 Credits",
              "CANM 200 History of Natural Medicine, 3 Credits",
              "CHIN 311 Chinese Culture, 3 Credits",
              "CHIN 321 Chinese Film:Culture & Society, 3 Credits",
              "COMM 252 Interpersonal Communication, 3 Credits",
              "ECON 130 Introduction to Economics, 3 Credits",
              "ECON 200 Principles of Macroeconomics, 3 Credits",
              "ECON 201 Principles of Microeconomics, 3 Credits",
              "ECON 205 Principles of Economics, 5 Credits",
              "ED 389 WE/Foundations of Education, 3 Credits",
              "HIST 1002 Revolt in History: Topics, 3 Credits",
              "HIST 1011 World Civilizations I, 3 Credits",
              "HIST 1012 World Civilizations II, 3 Credits",
              "HIST 102 Revolt:, 3 Credits",
              "HIST 104 US History I, 1607-1877, 3 Credits",
              "HIST 105 US History II, 1877-Present, 3 Credits",
              "HIST 1104 US History I, 3 Credits",
              "HIST 1105 US History II, 3 Credits",
              "HIST 111 World Civ before AD 1300, 3 Credits",
              "HIST 112 World Civ since AD 1300, 3 Credits",
              "HIST 1300 Cultural Explora San Francisco, 3 Credits",
              "HIST 131 World Civ before AD 500, 3 Credits",
              "HIST 132 World Civ AD 500 to 1700, 3 Credits",
              "HIST 133 World Civilizations since 1700, 3 Credits",
              "HIST 140 Latin Amer during Natl Period, 3 Credits",
              "HIST 141 East Asian Civilization I, 3 Credits",
              "HIST 142 East Asian Civilization II, 3 Credits",
              "HIST 151 Hist of Africa I (to 1800), 3 Credits",
              "HIST 152 Hist of Africa II (since 1800), 3 Credits",
              "HIST 1601 East Asia Civilizations I, 3 Credits",
              "HIST 1602 East Asian Civilizations II, 3 Credits",
              "HIST 1701 History of Africa I, 3 Credits",
              "HIST 1702 History of Africa II, 3 Credits",
              "HIST 1801 Latin Am During Nat'l Period, 3 Credits",
              "HIST 201 US History & Historiography I, 3 Credits",
              "HIST 2011 WE/World History I, 4 Credits",
              "HIST 2012 WE/World History II, 4 Credits",
              "HIST 202 US History & Historiography 2, 3 Credits",
              "HIST 211 WE/World Hist I:Dawn to AD1300, 4 Credits",
              "HIST 212 WE/World History II:1200 to Pr, 4 Credits",
              "HIST 3000 WE/Topics in World History, 4 Credits",
              "HIST 303 History Topics for Non-Majors, 3 Credits",
              "HIST 3085 WE/Global World War I, 4 Credits",
              "HIST 3100 WE/Topics in US History:, 4 Credits",
              "HIST 3103 WE/Historiography of the U.S., 4 Credits",
              "HIST 3104 WE/Modern US Historiography, 4 Credits",
              "HIST 313 WE/US Hist/Historiography 1877, 4 Credits",
              "HIST 314 WE/Modern US Historiography, 4 Credits",
              "HIST 3169 WE/Truman: Life & Presidency, 4 Credits",
              "HIST 3320 WE/Eugenics in America, 4 Credits",
              "HIST 3321 WE/Red Scares, 4 Credits",
              "HIST 3400 WE/European History Topics:, 4 Credits",
              "HIST 3410 WE/Ancient Greece, 4 Credits",
              "HIST 3415 WE/Ancient Rome, 4 Credits",
              "HIST 3420 WE/Medieval Europe I, 4 Credits",
              "HIST 3423 WE/Modern Europe II, 4 Credits",
              "HIST 3600 WE/Topics in Asian History:, 4 Credits",
              "HIST 3815 WE/Women in Latin Amer History, 4 Credits",
              "HIST 3825 WE/Mexican History, 4 Credits",
              "HIST 3850 WE/Latin American Revolutions, 4 Credits",
              "HIST 393 WE/History of Science I, 4 Credits",
              "HIST 394 WE/History of Science II, 4 Credits",
              "HLTH 255 Intro to Commun & Public Hlth, 3 Credits",
              "HLTH 270 Health Systems & Consumers, 3 Credits",
              "HS 010 Hist Mode Elective 100-200, 10 Credits",
              "HS 030 Hist Mode Elective 300-400, 10 Credits",
              "ITAL 324 Italian Civilization, 3 Credits",
              "JAPN 326 Japanese Society & Literature, 3 Credits",
              "JUST 205 Intro Criminal Justice Studies, 3 Credits",
              "LING 200 Introduction to Languages, 3 Credits",
              "LING 324 WE/Sociolinguistics, 4 Credits",
              "LING 325 WE/Language & Gender, 4 Credits",
              "LING 326 WE/Language & Ethnicity, 4 Credits",
              "LSP HS LSP: Historical Mode, 3 Credits",
              "LSP SS LSP: Social Scientific Mode, 3 Credits",
              "NASC 400 History of Science to 1700, 3 Credits",
              "NASC 401 History of Science since 1700, 3 Credits",
              "NU 250 Life Span Development, 3 Credits",
              "PHRE 305 Shamanism, 3 Credits",
              "POL 012 POL 161 Not MO Statute, 10 Credits",
              "POL 161 American Natl Government, 3 Credits",
              "POL 171 Intro to Political Science, 3 Credits",
              "POL 210 Law & Society, 3 Credits",
              "POL 250 Intro to Intl Relations, 3 Credits",
              "POL 251 Peace and Security, 3 Credits",
              "POL 252 Women, Gender, & Politics, 3 Credits",
              "POL 255 Intro to Intern'l Pol Economy, 3 Credits",
              "POL 262 State & Local Government, 3 Credits",
              "POL 325 U.S. Pol Inst: Struct,Hist,Evo, 3 Credits",
              "PSYC 166 General Psychology, 3 Credits",
              "SM 010 Soc Sci Mode Elect 100-200, 10 Credits",
              "SM 030 Soc Sci Mode Elect 300-400, 10 Credits",
              "SOAN 190 Introduction to Sociology, 3 Credits",
              "SOAN 191 Introduction to Anthropology, 3 Credits",
              "SOAN 215 Social Problems, 3 Credits",
              "SOAN 216 Sociology of Health & Illness, 3 Credits",
              "SOAN 217 Sociology of Sexualities, 3 Credits",
              "SOAN 220 World Prehistory, 3 Credits",
              "SOAN 232 Anthropology of Gender, 3 Credits",
              "SOAN 250 Global Focus, 3 Credits",
              "SOAN 253 Comparative Cultures, 3 Credits",
              "SOAN 260 Social Institutions, 3 Credits",
              "SOAN 265 Structured Inequalities, 3 Credits",
              "SOAN 267 Social Psychology, 3 Credits",
              "SOAN 297 Intro to Indigenous Americas, 3 Credits",
              "STEM 310 WE/History of Science I, 3 Credits",
              "STEM 311 WE/History of Science II, 3 Credits",
              "STEM 312 Science & Religion: Hist Pers, 3 Credits"
            ]
          }
        ]
      }
    ]
  },
  {
    "Perspective": "STEM Perspective",
    "Subsection": [
      {
        "Section": "Lab Science (4-5 Credits)",
        "Courses": [
          "AGSC 100 Food, Agri, Environ with Lab, 4 Credits",
          "AGSC 108 Intro to Agri Systems with Lab, 4 Credits",
          "BIOL 100 Biology with Lab, 4 Credits",
          "BIOL 103 General Botany with Lab, 4 Credits",
          "BIOL 104 Ecology & Evol of the Organism, 4 Credits",
          "BIOL 106 General Zoology with Lab, 4 Credits",
          "BIOL 107 Cells, Molecules and Genes, 4 Credits",
          "CHEM 100 Chem for Contemp Living w Lab, 4 Credits",
          "CHEM 120 Chemical Principles I with Lab, 5 Credits",
          "CHEM 121 Chemical Principles II w/ Lab, 5 Credits",
          "CHEM 122 Honors General Chemistry w Lab, 5 Credits",
          "CHEM 130 Chemical Principles I, 4 Credits",
          "CHEM 131 Chemical Principles II, 4 Credits",
          "CHEM 150 Hnrs Chem Contemp Living w Lab, 4 Credits",
          "ENVS 210 Environmental Science w/lab, 4 Credits",
          "LS 010 Life Science Elective 100-200, 10 Credits",
          "LS 030 Life Science Elective 300-400, 10 Credits",
          "LSP LS LSP: Scientific Life Sci Mode, 4 Credits",
          "LSP PS LSP:Scientific Phys Sci Mode, 4 Credits",
          "PHYS 100 Concepts in Physics with Lab, 4 Credits",
          "PHYS 105 Earth System Science, 4 Credits",
          "PHYS 131 Introduction to Astronomy, 4 Credits",
          "PHYS 132 Intro to Solar Systm Astronomy, 4 Credits",
          "PHYS 185 College Physics I with Lab, 4 Credits",
          "PHYS 186 College Physics II with Lab, 4 Credits",
          "PHYS 195 Physics I w Lab, 5 Credits",
          "PHYS 196 Physics II w Lab, 5 Credits",
          "PHYS 246 Astronomy I with Lab, 4 Credits",
          "PHYS 271 Physics for Scient. & Eng. I, 4 Credits",
          "PHYS 272 Physics for Scient. & Eng. II, 4 Credits",
          "PS 010 Physical Sci Elect 100-200, 10 Credits",
          "PS 030 Physical Sci Elect 300-400, 10 Credits"
        ]
      }
    ]
  },
  {
    "Perspective": "Arts & Humanities Perspective",
    "Subsection": [
      {
        "Section": "Arts & Humanities (9 Credits from two different prefixes)",
        "Courses": [
          "AF 010 Aesthetic:FA Elective 100-200, 10 Credits",
          "AF 030 Aesthetic:FA Elective 300-400, 10 Credits",
          "AL 010 Aesthetic:Lit Elective 100-200, 10 Credits",
          "AL 030 Aesthetic:Lit Elective 300-400, 10 Credits",
          "ART 101 Observational Drawing, 3 Credits",
          "ART 202 Figure Drawing, 3 Credits",
          "ART 203 Intro to the Visual Arts, 3 Credits",
          "ART 205 Ceramics I, 3 Credits",
          "ART 207 Fibers I, 3 Credits",
          "ART 211 3D Design, 3 Credits",
          "ART 216 Sculpture I, 3 Credits",
          "ART 217 Printmaking I, 3 Credits",
          "ART 218 Painting I, 3 Credits",
          "ART 221 Photography 1, 3 Credits",
          "ART 223 Global Art from 1400, 3 Credits",
          "ART 224 Non-Western Art, 3 Credits",
          "ART 305 Ceramics II, 3 Credits",
          "ART 307 Fibers II, 3 Credits",
          "ART 311 Printmaking II, 3 Credits",
          "ART 313 Photography II, 3 Credits",
          "ART 316 Sculpture II, 3 Credits",
          "ART 318 Painting II, 3 Credits",
          "ART 323 WE/Medieval Art, 3 Credits",
          "ART 324 WE/Renaissance Art, 3 Credits",
          "ART 325 WE/Modern Art, 3 Credits",
          "ART 326 Contemporary Art, 3 Credits",
          "ART 327 WE/Egyptian Art, 3 Credits",
          "ART 328 WE/The Art of Greece & Rome, 3 Credits",
          "ART 332 WE/Baroque Art, 3 Credits",
          "ART 333 WE/Islamic Art, 3 Credits",
          "ART 345 WE/History of Graphic Design, 3 Credits",
          "ART 428 WE/Topics in Art History, 3 Credits",
          "CHIN 311 Chinese Culture, 3 Credits",
          "CHIN 321 Chinese Film:Culture & Society, 3 Credits",
          "CLAS 261 Greek Lit in Translation, 3 Credits",
          "CLAS 262 Roman Lit in Translation, 3 Credits",
          "CLAS 310 Classical Antiquity on Screen, 3 Credits",
          "CLAS 361 Greek & Roman Mythology, 3 Credits",
          "CML 320 International Films, 3 Credits",
          "COMM 273 Oral Interpretation, 3 Credits",
          "CRWT 333 Studies in American Literature, 4 Credits",
          "CRWT 355 Intro to Lit Genres: Poetry, 4 Credits",
          "CRWT 356 Intro to Lit Genres: Novel, 4 Credits",
          "CRWT 357 Intro Lit Genres: Short Story, 4 Credits",
          "CRWT 358 Intro Lit Genres: Nonfiction, 4 Credits",
          "CRWT 359 Intro Lit Genres: Nonfiction, 3 Credits",
          "ENG 206 Topics in Forms & Genres, 3 Credits",
          "ENG 211 WE/Perspectives on Lit & Film, 3 Credits",
          "ENG 225 World Literatures: Chronology, 3 Credits",
          "ENG 226 World Literatures: Topics, 3 Credits",
          "ENG 228 WE/Animal Narratives, 3 Credits",
          "ENG 245 British Lit: Chronology, 3 Credits",
          "ENG 246 British Literatures: Topics, 3 Credits",
          "ENG 250 Shakespeare, 3 Credits",
          "ENG 266 American Literatures: Topics, 3 Credits",
          "ENG 280 WE/Film Form & Sense, 3 Credits",
          "ENG 306 WE/Studies in Women Writers, 4 Credits",
          "ENG 307 Studies in World Literature, 4 Credits",
          "ENG 308 Mythology, 4 Credits",
          "ENG 315 Studies in Shakespeare, 4 Credits",
          "ENG 316 Chaucer, 4 Credits",
          "ENG 320 Asian Literature, 4 Credits",
          "ENG 321 Internat'l Literatures: Topics, 4 Credits",
          "ENG 322 Studies in Cinema, 4 Credits",
          "ENG 325 Middle Eastern Literature, 4 Credits",
          "ENG 326 Diverse American Literature, 4 Credits",
          "ENG 330 N. American Indian Literature, 4 Credits",
          "ENG 331 Studies in African American Lt, 4 Credits",
          "ENG 333 Studies in American Literature, 4 Credits",
          "ENG 334 Studies Major American Authors, 4 Credits",
          "ENG 341 Old English Literature, 4 Credits",
          "ENG 342 Medieval Literature, 4 Credits",
          "ENG 343 British Renaissance Literature, 4 Credits",
          "ENG 344 British Renaissance Lit II, 3 Credits",
          "ENG 345 Restoration & 18th C Brit Lit, 4 Credits",
          "ENG 346 British Romantic Literature, 4 Credits",
          "ENG 347 British Victorian Literature, 4 Credits",
          "ENG 348 Studies in British Literature, 4 Credits",
          "ENG 349 Studies in Maj British Authors, 4 Credits",
          "ENG 351 Beowulf, 4 Credits",
          "ENG 353 American Authors, 4 Credits",
          "ENG 356 Intro Lit Genres: The Novel, 3 Credits",
          "ENG 357 Intro Lit Genres: Short Story, 3 Credits",
          "ENG 358 Intro Lit Genres: Nonfiction, 3 Credits",
          "ENG 365 WE/Folklore, 4 Credits",
          "ENG 366 Early American Literature, 4 Credits",
          "ENG 367 American Romanticism, 4 Credits",
          "ENG 368 American Realism & Naturalism, 4 Credits",
          "ENG 369 Modern American Literature, 4 Credits",
          "ENG 370 Contemporary American Lit, 4 Credits",
          "ENG 420 Theorizing Class in Lit:Topics, 4 Credits",
          "ENG 421 Studies in Literature &History, 4 Credits",
          "ENG 440 Studies in Lit & Geography, 4 Credits",
          "ENG 509 Topics:British & Commnwlth Lit, 4 Credits",
          "ENG 511 Topics in American Literature, 4 Credits",
          "GERM 332 Intro to German Literature I, 3 Credits",
          "GERM 333 Intro to German Literature II, 3 Credits",
          "ITAL 225 Italian Film, 3 Credits",
          "ITAL 326 Topics in Italian Culture, 3 Credits",
          "JAPN 323 Japanese Culture & Socioling, 3 Credits",
          "JAPN 324 Japanese Linguistics & Transl, 3 Credits",
          "JAPN 327 Japanese Film, 3 Credits",
          "LSP AF LSP: Aesthetic Fine Arts Mode, 3 Credits",
          "LSP AL LSP: Aesthetic Literature Mode, 3 Credits",
          "LSP PR LSP: Philosophical/Relig Mode, 3 Credits",
          "MUSI 101 Music Fundamentals, 3 Credits",
          "MUSI 103 Percussion Ensemble, 1 Credit",
          "MUSI 104 Brass Choir, 1 Credit",
          "MUSI 106 Jazz Ensemble, 1 Credit",
          "MUSI 107 Jazz Combos, 1 Credit",
          "MUSI 108 Jazz Lab Band, 1 Credit",
          "MUSI 109 President's String Quartet, 1 Credit",
          "MUSI 111 Chamber Ensemble, 1 Credit",
          "MUSI 116 Wind Symphony I, 1 Credit",
          "MUSI 117 Wind Symphony II, 1 Credit",
          "MUSI 118 Concert Band, 1 Credit",
          "MUSI 121 Marching Band, 1 Credit",
          "MUSI 122 Marching Percussion, 1 Credit",
          "MUSI 123 Color Guard, 1 Credit",
          "MUSI 145 Chorus, 1 Credit",
          "MUSI 146 Orchestra, 1 Credit",
          "MUSI 147 Voci Chamber Choir, 1 Credit",
          "MUSI 149 Cantoria, 1 Credit",
          "MUSI 203 Perspect in Music: Latin Amer, 3 Credits",
          "MUSI 204 Perspect in Music:West Thought, 3 Credits",
          "MUSI 205 Persp in Music: World Musics, 3 Credits",
          "MUSI 206 Persp in Music:Hollywd & Brdwy, 3 Credits",
          "MUSI 207 Persp in Music:Jazz & Amer Exp, 3 Credits",
          "MUSI 210 Perspective in Music: Hip-Hop, 3 Credits",
          "MUSI 303 Percussion Ensemble, Upper Div, 1 Credit",
          "MUSI 304 Brass Choir, Upper Division, 1 Credit",
          "MUSI 306 Jazz Ensemble: Upper Division, 1 Credit",
          "MUSI 307 Jazz Combos: Upper Division, 1 Credit",
          "MUSI 308 Jazz Lab Band: Upper Division, 1 Credit",
          "MUSI 309 Pres String Quartet: Upper Div, 1 Credit",
          "MUSI 311 Chamber Ensemble: Upper Div, 1 Credit",
          "MUSI 316 Wind Symphony I: Upper Div, 1 Credit",
          "MUSI 317 Wind Symphony ii: Upper Div, 1 Credit",
          "MUSI 318 Concert Band: Upper Division, 1 Credit",
          "MUSI 321 Marching Band: Upper Division, 1 Credit",
          "MUSI 322 Marching Percussion: Upper Div, 1 Credit",
          "MUSI 323 Color Guard: Upper Division, 1 Credit",
          "MUSI 339 Music Literature, 3 Credits",
          "MUSI 345 Chorus, Upper Division, 1 Credit",
          "MUSI 346 Orchestra, Upper Division, 1 Credit",
          "MUSI 347 Voci Chamber Choir, Upper Div, 1 Credit",
          "MUSI 349 Cantoria, Upper Division, 1 Credit",
          "PHRE 185 Exploring Religions, 3 Credits",
          "PHRE 186 Introduction to Philosophy, 3 Credits",
          "PHRE 188 Ethics, 3 Credits",
          "PHRE 210 Introduction to the Bible, 3 Credits",
          "PHRE 260 Religion and Film, 3 Credits",
          "PHRE 274 Faith & Reason in Christian Th, 3 Credits",
          "PHRE 285 Cults and Sects, 3 Credits",
          "PHRE 301 Christianity, 3 Credits",
          "PHRE 304 Religion & American Culture, 3 Credits",
          "PHRE 312 Japanese Religions, 3 Credits",
          "PHRE 316 Religions of China & Japan, 3 Credits",
          "PHRE 337 Early Modern Philosophy, 3 Credits",
          "PHRE 346 Stdys in Rel I: Chr, Is, Jud, 3 Credits",
          "PHRE 347 Stdys Rel II: East & Near East, 3 Credits",
          "PHRE 350 Biomedical Ethics, 3 Credits",
          "PHRE 356 Philosophy of Action, 3 Credits",
          "PHRE 360 African American Religions, 3 Credits",
          "PHRE 370 Epistemology, 3 Credits",
          "PHRE 384 Philosophy of Social Science, 3 Credits",
          "PHRE 386 Studies in Philosophy/Religion, 3 Credits",
          "PR 010 PHRE Mode Elect 100-200, 10 Credits",
          "PR 030 PHRE Mode Elect 300-400, 10 Credits",
          "SPAN 353 Intro to Hispanic Literature, 3 Credits",
          "SPAN 460 Srvy of Span Peninsular Lit, 3 Credits",
          "SPAN 461 WE/Survey of Spanish Amer Lit, 3 Credits",
          "THEA 275 Intro to the Theatre Arts, 3 Credits",
          "THEA 371 History & Lit of Theatre I, 3 Credits",
          "THEA 372 History & Lit of Theatre II, 3 Credits",
          "THEA 374 Contemporary Trends in Theatre, 3 Credits",
          "THEA 393 Lighting Design, 3 Credits",
          "THEA 420 WE/Playwriting, 3 Credits",
          "THEA 480 Scene Design, 3 Credits"
        ]
      }
    ]
  },
  {
    "Perspective": "Statistics Perspective",
    "Subsection": [
      {
        "Section": "Statistics (3 Credits)",
        "Courses": [
          "STAT 190 Basic Statistics, 3 Credits",
          "STAT 290 Statistics, 3 Credits"
        ]
      }
    ]
  },
  {
    "Perspective": "Interconnecting Perspectives",
    "Subsection": [
      {
        "Section": "JINS (Interdisciplinary WE Junior Seminar)",
        "Courses": [
          "JINS 300 WE/Cultural Crossroads, 3 Credits",
          "JINS 3000 WE/Fringe Thought, 3 Credits",
          "JINS 3001 WE/ Human Consciousness, 3 Credits",
          "JINS 3002 WE/World of Divine Comedy, 3 Credits",
          "JINS 3003 WE/The Bible as Literature, 3 Credits",
          "JINS 3004 WE/Athenian Drama In/Out of Co, 3 Credits",
          "JINS 3005 WE/William Blake's Apocalyptic, 3 Credits",
          "JINS 3006 WE/Tabletop Role Playing Games, 3 Credits",
          "JINS 301 WE/Music in Religious Thought, 3 Credits",
          "JINS 302 WE/Wilderness Leadership, 3 Credits",
          "JINS 303 WE/Computers & Natural Lang, 3 Credits",
          "JINS 304 WE/Native American Conflict, 3 Credits",
          "JINS 305 WE/Issues in Democratic Inst, 3 Credits",
          "JINS 306 WE/Rock Music, 3 Credits",
          "JINS 307 WE/Friendship, 3 Credits",
          "JINS 308 WE/US Immigrants & Imgnt Writ, 3 Credits",
          "JINS 309 WE/Decision Making Seminar, 3 Credits",
          "JINS 310 WE/Ancient Historians, 3 Credits",
          "JINS 311 WE/Race, Class, & Gender, 3 Credits",
          "JINS 312 WE/American Social Character, 3 Credits",
          "JINS 313 WE/Bloomsbury, 3 Credits",
          "JINS 314 WE/Economics of Gender, 3 Credits",
          "JINS 315 WE/Nuclear Weaponry, 3 Credits",
          "JINS 316 WE/Portrayals of Women, 3 Credits",
          "JINS 317 WE/Intercultural Women's Mvmnt, 3 Credits",
          "JINS 318 WE/Classical Athenian Humanism, 3 Credits",
          "JINS 319 WE/Human & Computer Cognition, 3 Credits",
          "JINS 320 WE/Development of the Book, 3 Credits",
          "JINS 321 WE/Leadership Analysis, 3 Credits",
          "JINS 322 WE/Architecture: Forms & Struc, 3 Credits",
          "JINS 323 WE/Dress & Self Image, 3 Credits",
          "JINS 324 WE/Contexts of Disability, 3 Credits",
          "JINS 325 WE/Rural America, 3 Credits",
          "JINS 326 WE/On Human Nature, 3 Credits",
          "JINS 327 WE/Illuminations, 3 Credits",
          "JINS 328 WE/Exploration & Discovery, 3 Credits",
          "JINS 329 WE/Language & Meaning, 3 Credits",
          "JINS 330 WE/Environmental Economics, 3 Credits",
          "JINS 331 WE/Chemistry of Art, 3 Credits",
          "JINS 332 WE/Death & Dying, 3 Credits",
          "JINS 333 WE/Conflict, Coop, Choice, 3 Credits",
          "JINS 334 WE/Geometry of the Universe, 3 Credits",
          "JINS 335 WE/Ecology vs Land Use, 3 Credits",
          "JINS 336 WE/Environment, 3 Credits",
          "JINS 337 WE/Musical Theatre, 3 Credits",
          "JINS 338 WE/Race & Ethnicity, 3 Credits",
          "JINS 339 WE/Gender & Culture, 3 Credits",
          "JINS 340 WE/German-Jewish Identities, 3 Credits",
          "JINS 341 WE/Sport & Society, 3 Credits",
          "JINS 342 WE/The Indo-Europeans, 3 Credits",
          "JINS 343 WE/Horse in Art, Sci & Hist, 3 Credits",
          "JINS 344 WE/Salome & John the Baptist, 3 Credits",
          "JINS 345 WE/From Page to Stage & Screen, 3 Credits",
          "JINS 346 WE/Varieties of Non-Violence, 3 Credits",
          "JINS 347 WE/Religion, Health, & Healing, 3 Credits",
          "JINS 348 WE/Visual Wrld: Color/Symmetry, 3 Credits",
          "JINS 349 WE/Bodylore/Brainlore, 3 Credits",
          "JINS 350 WE/Science & Society, 3 Credits",
          "JINS 351 WE/Faust Tradition, 3 Credits",
          "JINS 352 WE/Why You're Wrong, 3 Credits",
          "JINS 353 WE/Ethics & Human Genome Proj, 3 Credits",
          "JINS 354 WE/Insects, Disease & Humans, 3 Credits",
          "JINS 355 WE/Creativity in Arts & Sci, 3 Credits",
          "JINS 356 WE/Art & Science of Humor, 3 Credits",
          "JINS 357 WE/Bayou Blues: Fren Music LA, 3 Credits",
          "JINS 358 WE/Textiles as Cultrl Document, 3 Credits",
          "JINS 359 WE/Exploration Origins of Life, 3 Credits",
          "JINS 360 WE/Amish History and Culture, 3 Credits",
          "JINS 361 WE/Innovations of War, 3 Credits",
          "JINS 362 WE/Extraterrestrial Life, 3 Credits",
          "JINS 363 WE/Class in America, 3 Credits",
          "JINS 364 WE/The Aesthetics of Food, 3 Credits",
          "JINS 365 WE/Science and Literature, 3 Credits",
          "JINS 366 WE/Potent Potables: Reflection, 3 Credits",
          "JINS 367 WE/The Paradoxes of Infinity, 3 Credits",
          "JINS 368 WE/Women and Science, 3 Credits",
          "JINS 369 WE/Why We Fight, 3 Credits",
          "JINS 370 Econ Growth Polit Instability, 3 Credits",
          "JINS 371 WE/Music & Political Protest, 3 Credits",
          "JINS 372 WE/Communication & the Face, 3 Credits",
          "JINS 373 WE/Stress in America, 3 Credits",
          "JINS 374 WE/The Parenting Process, 3 Credits",
          "JINS 375 WE/Weird Science, 3 Credits",
          "JINS 376 WE/Women's Health, 3 Credits",
          "JINS 377 WE/Serial Killers & Psychopths, 3 Credits",
          "JINS 378 WE/Visual Mus Mimetic-Abstract, 3 Credits",
          "JINS 379 The Epic Tradition, 3 Credits",
          "JINS 380 Roads to Dictatorship-Germany, 3 Credits",
          "JINS 381 Public Issues & Political Rhet, 3 Credits",
          "JINS 382 WE/The Computerized Society, 3 Credits",
          "JINS 383 WE/Years of Change: 1968, 3 Credits",
          "JINS 384 WE/Drugs Society Crime & Trtmt, 3 Credits",
          "JINS 385 WE/Childrens Lit & Contro Iss, 3 Credits",
          "JINS 386 WE/Christmas:CultureContrvrsy, 3 Credits",
          "JINS 387 WE/Reel Africa:History in Film, 3 Credits",
          "JINS 388 WE/Hunting in America, 3 Credits",
          "JINS 389 WE/Influence of the Gene, 3 Credits",
          "JINS 390 WE/Prisoner Reentry-Policy&Pro, 3 Credits",
          "JINS 391 WE/Contentious Politics, 3 Credits",
          "JINS 392 WE/Nature and Human Nature, 3 Credits",
          "JINS 393 WE/Historic Trials, 3 Credits",
          "JINS 394 WE/Biography:, 3 Credits",
          "JINS 395 WE/Food Systems & Sustainabil, 3 Credits",
          "JINS 396 WE/Languages of Spec Fiction, 3 Credits",
          "JINS 397 WE/Visualizing the Narrative, 3 Credits",
          "JINS 398 WE/Hollywood & Human Perform, 3 Credits",
          "JINS 399 WE/Epidemic:, 3 Credits",
          "JINS 400 WE/Fringe Thought, 3 Credits",
          "JINS 401 WE/The World of Divine Comedy, 3 Credits"
        ]
      }
    ]
  }
]

sample_plan_urls = [
    {
        "major": "Accounting (BS)",
        "url": "http://www.truman.edu/fouryearplan/accounting-major/"
    },
    {
        "major": "Agricultural Science (BS), Business Track",
        "url": "http://www.truman.edu/fouryearplan/agricultural-science-business-track/"
    },
    {
        "major": "Agricultural Science (BS), Science Track",
        "url": "http://www.truman.edu/fouryearplan/agricultural-science-science-track/"
    },
    {
        "major": "Agricultural Science (BS), Pre-Education Track",
        "url": "https://www.truman.edu/fouryearplan/agricultural-science-pre-education-track/"
    },
    {
        "major": "Applied Linguistics/TESOL (BA)",
        "url": "https://www.truman.edu/fouryearplan/applied-linguistics-tesol-ba/"
    },
    {
        "major": "Art (BFA), Design Track 1 - Graphic Design",
        "url": "http://www.truman.edu/fouryearplan/art-bfa-design/"
    },
    {
        "major": "Art (BFA), Design Track 2 - 3D Modeling & Animation",
        "url": "http://www.truman.edu/fouryearplan/art-bfa-3d-design/"
    },
    {
        "major": "Art (BFA), Studio Art",
        "url": "http://www.truman.edu/fouryearplan/art-bfa-studio/"
    },
    {
        "major": "Art (BA), Art History Track",
        "url": "http://www.truman.edu/fouryearplan/art-history-ba/"
    },
    {
        "major": "Art (BA), Studio Track",
        "url": "http://www.truman.edu/fouryearplan/art-ba-studio/"
    },
    {
        "major": "Art (BFA), Design ONLINE, New Major: Full-time",
        "url": "https://www.truman.edu/fouryearplan/design-bfa-online/"
    },
    {
        "major": "Art (BFA), Design ONLINE, AA Degree: Full-time",
        "url": "https://www.truman.edu/fouryearplan/design-bfa-online-aa-degree/"
    },
    {
        "major": "Art (BFA), Design ONLINE, New Major: Part-time",
        "url": "https://www.truman.edu/majors-programs/majors-minors/online-bfa-design/design-bfa-online-4-year-plans/#details-0-2"
    },
    {
        "major": "Art (BFA), Design ONLINE, AA Degree Part-time",
        "url": "https://www.truman.edu/majors-programs/majors-minors/online-bfa-design/design-bfa-online-4-year-plans/#details-0-3"
    },
    {
        "major": "Biochemistry and Molecular Biology (BS)",
        "url": "http://www.truman.edu/fouryearplan/biochemistry-and-molecular-biology-bs/"
    },
    {
        "major": "Biochemistry and Molecular Biology (BS) – Alternative Plan",
        "url": "https://www.truman.edu/fouryearplan/biochemistry-and-molecular-biology-bs-alternative-plan/"
    },
    {
        "major": "Biology (BS/BA)",
        "url": "http://www.truman.edu/fouryearplan/biology-bsba/"
    },
    {
        "major": "Business Administration (BS/BA), Finance",
        "url": "http://www.truman.edu/fouryearplan/business-administration-bsba-finance/"
    },
    {
        "major": "Business Administration (BA), International Business",
        "url": "http://www.truman.edu/fouryearplan/business-administration-ba-international-business/"
    },
    {
        "major": "Business Administration (BS/BA), Management",
        "url": "http://www.truman.edu/fouryearplan/business-administration-bsba-management/"
    },
    {
        "major": "Business Administration (BS/BA), Marketing",
        "url": "http://www.truman.edu/fouryearplan/business-administration-bsba-marketing/"
    },
    {
        "major": "Cannabis and Natural Medicinals (BS, Analytical Science)",
        "url": "https://www.truman.edu/fouryearplan/cannabis-and-natural-medicinals-analytical-science/"
    },
    {
        "major": "Cannabis and Natural Medicinals (BS, Business and Entrepreneurship)",
        "url": "https://www.truman.edu/fouryearplan/cannabis-and-natural-medicinals-business-and-entrepreneurship/"
    },
    {
        "major": "Cannabis and Natural Medicinals (BS, Cultivation)",
        "url": "https://www.truman.edu/fouryearplan/cannabis-and-natural-medicinals-cultivation/"
    },
    {
        "major": "Cannabis and Natural Medicinals (BS, Society and Philosophy)",
        "url": "https://www.truman.edu/fouryearplan/cannabis-and-natural-medicinals-major-society-philosophy"
    },
    {
        "major": "Chemistry (BS)",
        "url": "http://www.truman.edu/fouryearplan/chemistry-bs/"
    },
    {
        "major": "Classics (BA), Focus on Language",
        "url": "http://www.truman.edu/fouryearplan/classics-ba/"
    },
    {
        "major": "Classics (BA), Focus on Culture",
        "url": "https://www.truman.edu/fouryearplan/classics-ba-culture/"
    },
    {
        "major": "Classics (BA), Pre-MAE Latin",
        "url": "https://www.truman.edu/fouryearplan/classics-ba-pre-mae-latin/"
    },
    {
        "major": "Communication (BA)",
        "url": "http://www.truman.edu/fouryearplan/communication-ba/"
    },
    {
        "major": "Communication Disorders (BS/BA)",
        "url": "http://www.truman.edu/fouryearplan/communication-disorders-bsba/"
    },
    {
        "major": "Computer Science (BS)",
        "url": "http://www.truman.edu/fouryearplan/computer-science-bs/"
    },
    {
        "major": "Creative Writing (BFA)",
        "url": "http://www.truman.edu/fouryearplan/creative-writing-bfa/"
    },
    {
        "major": "Criminal Justice Studies (BS), Law & Society Concentration",
        "url": "https://www.truman.edu/fouryearplan/criminal-justice-studies-law-society-concentration/"
    },
    {
        "major": "Criminal Justice Studies (BS), Criminological Theory & Research Concentration",
        "url": "https://www.truman.edu/fouryearplan/criminal-justice-studies-criminological-theory-research-concentration/"
    },
    {
        "major": "Criminal Justice Studies (BS), Forensic Investigation Concentration w/ Forensic Science minor Track I - Forensic DNA Lab-oriented",
        "url": "https://www.truman.edu/fouryearplan/criminal-justice-studies-forensic-investigation-concentration-w-forensic-science-minor-track-i-forensic-dna-lab-oriented/"
    },
    {
        "major": "Criminal Justice Studies (BS), Forensic Investigation Concentration w/ Forensic Science minor Track II - Forensic Chemistry Lab-oriented",
        "url": "https://www.truman.edu/fouryearplan/criminal-justice-studies-forensic-investigation-concentration-w-forensic-science-minor-track-ii-forensic-chemistry-lab-oriented/"
    },
    {
        "major": "Criminal Justice Studies (BS), Criminal Justice Administration Concentration",
        "url": "https://www.truman.edu/fouryearplan/criminal-justice-studies-criminal-justice-administration-concentration/"
    },
    {
        "major": "Economics (BA)",
        "url": "http://www.truman.edu/fouryearplan/economics-ba/"
    },
    {
        "major": "Economics (BS)",
        "url": "http://www.truman.edu/fouryearplan/economics-bs/"
    },
    {
        "major": "Economics (BS), PhD Prep",
        "url": "http://www.truman.edu/fouryearplan/economics-bs-phd-prep/"
    },
    {
        "major": "English (BA)",
        "url": "http://www.truman.edu/fouryearplan/english-ba/"
    },
    {
        "major": "Exercise Science (BS), Pre-Medical Sciences",
        "url": "https://www.truman.edu/fouryearplan/exercise-science-bs-pre-medical-sciences/"
    },
    {
        "major": "Exercise Science (BS), Applied/Athletic Training",
        "url": "https://www.truman.edu/fouryearplan/exercise-science-bs-applied-athletic-training/"
    },
    {
        "major": "Exercise Science and Athletic Training 3+2",
        "url": "https://www.truman.edu/fouryearplan/exercise-science-and-athletic-training/"
    },
    {
        "major": "Exercise Science (BS) and MAE Physical Education",
        "url": "https://www.truman.edu/fouryearplan/exercise-science-bs-and-mae-physical-education/"
    },
    {
        "major": "French (Modern Language BA)",
        "url": "http://www.truman.edu/fouryearplan/french-ba/"
    },
    {
        "major": "German (Modern Language BA)",
        "url": "http://www.truman.edu/fouryearplan/german-ba/"
    },
    {
        "major": "Health Science (BS), Community, Worksite, and Public Health",
        "url": "http://www.truman.edu/fouryearplan/health-science-bs-community-worksite-public-health/"
    },
    {
        "major": "Health Science (BS), Pre-Med",
        "url": "http://www.truman.edu/fouryearplan/health-science-bs-pre-med/"
    },
    {
        "major": "Health Science (BS), Pre-Occupational Therapy/Pre-Athletic Training",
        "url": "http://www.truman.edu/fouryearplan/health-science-bs-pre-occupational-therapypre-athletic-training/"
    },
    {
        "major": "History (BS/BA)",
        "url": "http://www.truman.edu/fouryearplan/history-bsba/"
    },
    {
        "major": "Linguistics (BS)",
        "url": "http://www.truman.edu/fouryearplan/linguistics-bs/"
    },
    {
        "major": "Mathematics (BS/BA)",
        "url": "http://www.truman.edu/fouryearplan/mathematics-bsba/"
    },
    {
        "major": "Mathematics (BS/BA), Actuarial Science",
        "url": "https://www.truman.edu/fouryearplan/mathematics-ba-bs-actuarial-science/"
    },
    {
        "major": "Mathematics (BS/BA), Pre-MAE",
        "url": "https://www.truman.edu/fouryearplan/mathematics-ba-bs-pre-mae/"
    },
    {
        "major": "Mathematics (BS/BA), Graduate School Bound Students",
        "url": "https://www.truman.edu/fouryearplan/mathematics-ba-bs-graduate-school-bound/"
    },
    {
        "major": "Music Business (BS)",
        "url": "https://www.truman.edu/fouryearplan/music-business-bs/"
    },
    {
        "major": "Music (BA) Pre-Certification - Instrumental",
        "url": "http://www.truman.edu/fouryearplan/music-ba-pre-certification-instrumental/"
    },
    {
        "major": "Music (BA), Pre-Certification - Vocal",
        "url": "http://www.truman.edu/fouryearplan/music-ba-pre-certification-vocal/"
    },
    {
        "major": "Music (BA), General",
        "url": "http://www.truman.edu/fouryearplan/music-ba-general/"
    },
    {
        "major": "Music (BA), Liberal Arts",
        "url": "http://www.truman.edu/fouryearplan/music-ba-liberal-arts/"
    },
    {
        "major": "Music (BM), Composition",
        "url": "http://www.truman.edu/fouryearplan/music-bm-composition/"
    },
    {
        "major": "Music (BM), Performance",
        "url": "http://www.truman.edu/fouryearplan/music-bm-performance/"
    },
    {
        "major": "Music Therapy (BS)",
        "url": "http://www.truman.edu/fouryearplan/music-therapy-bs/"
    },
    {
        "major": "Nursing (BSN)",
        "url": "http://www.truman.edu/fouryearplan/nursing-bsn/"
    },
    {
        "major": "Nursing (ABSN)",
        "url": "http://www.truman.edu/fouryearplan/nursing-absn/"
    },
    {
        "major": "Philosophy and Religion (BS/BA)",
        "url": "http://www.truman.edu/fouryearplan/philosophy-religion-ba/"
    },
    {
        "major": "Physics (BA)-Start w/ Calc I",
        "url": "https://www.truman.edu/fouryearplan/physics-ba/"
    },
    {
        "major": "Physics (BA)-Start w/ Calc II",
        "url": "https://www.truman.edu/fouryearplan/physics-ba-calculus-2/"
    },
    {
        "major": "Physics (BS, General Physics Track)-Start w/ Calc I",
        "url": "https://www.truman.edu/fouryearplan/physics-bs/"
    },
    {
        "major": "Physics (BS, General Physics Track)-Start w/ Calc II",
        "url": "https://www.truman.edu/fouryearplan/physics-bs-calculus-2/"
    },
    {
        "major": "Physics (BS, Astrophysics Track)-Start w/ Calc I",
        "url": "https://www.truman.edu/fouryearplan/physics-bs-astro-track/"
    },
    {
        "major": "Physics (BS, Astrophysics Track)-Start w/ Calc II",
        "url": "https://www.truman.edu/fouryearplan/physics-bs-astro-track-calc-ii/"
    },
    {
        "major": "Dual Physics/Engineering-Start w/ Calc I",
        "url": "http://www.truman.edu/fouryearplan/physics-engineering-ba-calculus-1/"
    },
    {
        "major": "Dual Physics/Engineering-Start w/ Calc II",
        "url": "https://www.truman.edu/fouryearplan/physics-engineering-calc-2/"
    },
    {
        "major": "Pre-Engineering, Start with Calculus I",
        "url": "https://www.truman.edu/fouryearplan/physics-pre-engineering/"
    },
    {
        "major": "Pre-Engineering, Start with Calculus II",
        "url": "https://www.truman.edu/fouryearplan/physics-pre-engineering-calc-2/"
    },
    {
        "major": "Political Science and International Relations (BS/BA)",
        "url": "http://www.truman.edu/fouryearplan/political-science-bsba/"
    },
    {
        "major": "Psychology (BS/BA)",
        "url": "http://www.truman.edu/fouryearplan/psychology-bs/"
    },
    {
        "major": "Sociology/Anthropology (BS/BA)",
        "url": "http://www.truman.edu/fouryearplan/sociologyanthropology-bsba/"
    },
    {
        "major": "Spanish (Modern Language BA), Starting in 101",
        "url": "http://www.truman.edu/fouryearplan/spanish-ba-starting-in-101/"
    },
    {
        "major": "Spanish (Modern Language BA), Starting in 201",
        "url": "http://www.truman.edu/fouryearplan/spanish-201/"
    },
    {
        "major": "Spanish (Modern Language BA), Starting in 330",
        "url": "http://www.truman.edu/fouryearplan/spanish-ba-starting-in-330/"
    },
    {
        "major": "Statistics (BA)",
        "url": "http://www.truman.edu/fouryearplan/statistics-ba"
    },
    {
        "major": "Statistics (BS)",
        "url": "http://www.truman.edu/fouryearplan/statistics-bs/"
    },
    {
        "major": "Statistics (BS), Data Science",
        "url": "http://www.truman.edu/fouryearplan/statistics-bs-data-science/"
    },
    {
        "major": "Statistics (BS), Data Science; assumes MATH 198 and STAT 190 credit, as well as Minor in Computer Science",
        "url": "https://www.truman.edu/fouryearplan/statistics-bs-data-science-math-stat-credit/"
    },
    {
        "major": "Statistics (BS), Classical; assumes credit for STAT 190 and MATH 198",
        "url": "https://www.truman.edu/fouryearplan/statistics-bs-classical-math-stat-credit/"
    },
    {
        "major": "Theatre (BA)",
        "url": "http://www.truman.edu/fouryearplan/theater-ba/"
    },
    {
        "major": "Theatre (BA) and Musical Theatre Minor",
        "url": "https://www.truman.edu/fouryearplan/theater-ba-and-musical-theatre-minor/"
    }
]

class RecommendedCourse(BaseModel):
    course_code: str
    semester: int
    reason: str

class AdvisorResponse(BaseModel):
    recommended_courses: List[RecommendedCourse]
    text: str

#parsedDegreeWorks = parse_degreeworks_pdf("./degreeworks-data/letter-p.pdf")
with open("./parsedDegree/gpt4o_optimized.json", "r") as f:
    parsedDegreeWorks = json.load(f)

@tool
def get_parsed_degreeworks() -> dict:
    """Return the DegreeWorks audit (dict)."""
    return parsedDegreeWorks

@tool
def get_sample_plan_urls() -> list[dict]:
    """Return the sample plan URLs (array of dicts)."""
    return sample_plan_urls

@tool
def get_truman_req() -> list[dict]:
    """Return the Truman requirements of Disciplinary Perspectives or other Truman requirements (array of dicts)."""
    return truman_req

@tool
def scrape_sampleplan(url: str) -> dict:
    """Scrape Truman's sample plan based on the URLs in samplePlanUrls. Parse and return a string of JSON"""
    return scrape_sample_plan(url)


TOOLS = [get_parsed_degreeworks, get_sample_plan_urls, get_truman_req, scrape_sampleplan]

llm = ChatOpenAI(api_key=api_key, model_name="gpt-5")

OLD_PROMPT = """You are an expert AI academic advisor for Truman State University students. 
Your goal is to provide accurate, structured course planning advice based on the student's DegreeWorks audit and sample plans.

You have access to the following tools:
- get_parsed_degreeworks() -> dict
- get_sample_plan_urls() -> list[dict]
- get_truman_req() -> list[dict]
- scrape_sampleplan(url: str) -> dict
- (Optional later: scrape_rate_my_prof(course_code: str) -> list)

REASONING AND ACTION STEPS:

1. Call get_parsed_degreeworks() to retrieve the DegreeWorks JSON to determine:
- Completed courses
- Courses in progress
- Missing requirements and electives

2. Identify missing requirements and the types of courses the student should take next.

3. Call get_sample_plan_urls() and select only the relevant major and minor URLs. 
- Use scrape_sampleplan(url) to obtain sample plan JSON.
- Use this JSON to determine:
- Which courses satisfy missing major/minor requirements.
- Which courses require prerequisites. Courses appearing in the 3rd semester or later are assumed to have prerequisites.
- Only recommend a course if prerequisites are met (completed in DegreeWorks or earlier semesters).

4. For general education, missing electives, or courses outside the student's major/minor:
- Call get_truman_req() and filter only the relevant perspectives or sections.
- Prioritize courses:
1. Intro-level courses with numbers below 200.
2. Courses that appear at most in the 2nd semester of that subject’s sample plan.
- Avoid recommending advanced courses that are likely to have prerequisites.

5. If any course in the sample plan is a placeholder (e.g., "Elective", "Dialogues Curriculum course", "CS XXX"):
- Replace it with a valid course.
- Priority for replacements:
1. Missing courses from DegreeWorks recommendations.
2. Courses from Truman requirements JSON (`get_truman_req()`).
3. Other sample plans of other majors/minors (`get_sample_plan_urls()` + `scrape_sampleplan(url)`).
- Always ensure replacement courses have a valid prefix + number (e.g., CS 310).
- Never leave placeholders in the final recommended_courses output.

6. Assign courses to the next available semester, balancing workload and respecting a maximum of 17 credits per semester (unless the user explicitly requests otherwise).

7. Recommend courses clearly, intelligently, and dynamically based on student preferences.

8. Never invent courses or requirements. If info is missing, acknowledge it and suggest alternatives.

**CRITICAL OUTPUT FORMAT RULES:**
- Your ENTIRE response must be ONLY a valid JSON object - nothing before it, nothing after it
- All human-readable text, explanations, markdown, course justifications, and advice MUST go in the "text" field
- The "recommended_courses" array should contain only structured course objects
- Do NOT use code blocks, backticks, or any formatting around the JSON
- Start immediately with { and end with }
- Example of CORRECT output: 
{"recommended_courses": [{"course_code": "CS 180", "semester": 1, "reason": "Required for major"}], "text": "## Your Course Plan\\n\\nBased on your DegreeWorks audit, I recommend..."}

CRITICAL RULES:

- Only return valid courses with prefix + number.
- Filter tools output to only relevant majors/minors or perspectives to save tokens.
- Replace **all placeholders**; never leave them in the output.
- Respect maximum credit per semester unless explicitly instructed otherwise.
- Consider prerequisites for all recommended courses:
- Major/minor courses: check semester position in sample plan.
- Non-major courses: prioritize intro-level courses below 200 and appearing at most in semester 2.
- Always maintain JSON validity.
- Do NOT output any text outside of the JSON.

Always ensure the JSON is structured, complete, and accurate.
"""

SYSTEM_PROMPT = """You are an expert AI academic advisor for Truman State University students. 
Your goal is to provide accurate, structured course planning advice based on the student's DegreeWorks audit and sample plans.

You have access to the following tools:
- get_parsed_degreeworks() -> dict
- get_sample_plan_urls() -> list[dict]
- get_truman_req() -> list[dict]
- scrape_sampleplan(url: str) -> dict
- (Optional later: scrape_rate_my_prof(course_code: str) -> list)

REASONING AND ACTION STEPS:

1. Call get_parsed_degreeworks() to retrieve the DegreeWorks JSON to determine:
- Completed courses
- Courses in progress
- Missing requirements and electives
- Student's current major/minor

2. Identify missing requirements and the types of courses the student should take next.

3. COURSE ELIGIBILITY SAFETY CHECK - CRITICAL RULES:
- **For courses in student's MAJOR/MINOR**: 
  - Check the sample plan semester position
  - Courses in semester 3+ = assume prerequisites needed
  - Only recommend if prerequisites appear completed in DegreeWorks or earlier semesters

- **For courses OUTSIDE student's major/minor (electives, gen eds)**:
  - **STRICTLY prioritize**: Courses numbered 100-199 (introductory level)
  - **Allow only if no 100-level alternatives**: Courses numbered 200-299, but ONLY if they appear in semester 1-2 of that subject's sample plan
  - **NEVER recommend**: Courses numbered 300+ for non-major/non-minor students
  - **Exception**: Only if explicitly requested AND prerequisites verified completed

4. Call get_sample_plan_urls() and select only the relevant major and minor URLs. 
- Use scrape_sampleplan(url) to obtain sample plan JSON.
- Use this JSON to determine course sequencing and prerequisites.

5. For general education, missing electives, or courses outside the student's major/minor:
- Call get_truman_req() and filter only the relevant perspectives or sections.
- **Apply strict filters**:
  - First pass: Only courses numbered 100-199
  - Second pass: Only 200-level courses that appear in semester 1-2 of their subject's sample plan
  - Exclude all 300+ level courses for non-majors

6. COURSE LEVEL VALIDATION CHECK - Before recommending any course:
- **If course is 300+**: Must be in student's major/minor AND appear in semester 3+ of sample plan AND prerequisites likely met
- **If course is 200-299**: For non-majors, must appear in semester 1-2 of that subject's sample plan
- **If course is 100-199**: Generally safe to recommend

7. If any course in the sample plan is a placeholder (e.g., "Elective", "Dialogues Curriculum course", "CS XXX"):
- Replace it with a valid course following the safety rules above
- Priority for replacements:
  1. Missing courses from DegreeWorks recommendations (following safety rules)
  2. Courses from Truman requirements JSON (following safety rules)
  3. Other sample plans (following safety rules)

8. Assign courses to the next available semester, balancing workload and respecting a maximum of 17 credits per semester.

9. **FINAL SAFETY CHECK**: Before outputting, verify each recommended course:
- Major/minor courses: Check semester position and prerequisite likelihood
- Non-major courses: Must be 100-level OR 200-level in semester 1-2
- NEVER include 300+ level courses for non-majors without explicit prerequisite verification

10. Never invent courses or requirements. If info is missing, acknowledge it and suggest alternatives.


**CRITICAL OUTPUT FORMAT RULES:**
- Your ENTIRE response must be ONLY a valid JSON object - nothing before it, nothing after it
- All human-readable text, explanations, markdown, course justifications, and advice MUST go in the "text" field
- The "recommended_courses" array should contain only structured course objects
- Do NOT use code blocks, backticks, or any formatting around the JSON
- Start immediately with { and end with }
- Example of CORRECT output: 
{"recommended_courses": [{"course_code": "CS 180", "semester": 1, "reason": "Required for major"}], "text": "## Your Course Plan\\n\\nBased on your DegreeWorks audit, I recommend..."}

CRITICAL RULES:

- Only return valid courses with prefix + number.
- Filter tools output to only relevant majors/minors or perspectives to save tokens.
- Replace **all placeholders**; never leave them in the output.
- Respect maximum credit per semester unless explicitly instructed otherwise.
- Consider prerequisites for all recommended courses:
- Major/minor courses: check semester position in sample plan.
- Non-major courses: prioritize intro-level courses below 200 and appearing at most in semester 2.
- Always maintain JSON validity.
- Do NOT output any text outside of the JSON.

Always ensure the JSON is structured, complete, and accurate.
"""


NEW_PROMPT = """You are an expert AI academic advisor for Truman State University students. 
Your goal is to provide accurate, comprehensive course planning advice based on the student's DegreeWorks audit, sample plans, and Truman requirements.

AVAILABLE TOOLS:
- get_parsed_degreeworks() -> dict: Returns student's completed courses, in-progress courses, and missing requirements
- get_sample_plan_urls() -> list[dict]: Returns all available sample plan URLs for majors and minors
- get_truman_req() -> list[dict]: Returns general education and university-wide course requirements
- scrape_sampleplan(url: str) -> dict: Returns detailed course sequence for a specific major/minor
- scrape_rate_my_prof(course_code: str) -> list (optional): Returns professor ratings for a course

===============================================================================
CRITICAL: UNDERSTANDING USER REQUESTS
===============================================================================

When a user asks for a "4 year plan" or "plan out my remaining semesters":
- Calculate how many semesters remain until graduation (typically 8 semesters for 4 years)
- Plan EVERY SINGLE SEMESTER with 15-17 credits each
- If user is a sophomore, plan 6 remaining semesters (3 years)
- If user is a junior, plan 4 remaining semesters (2 years)
- Continue planning until you've recommended enough credits to graduate (typically 120 total)

DO NOT stop after just 2-3 semesters. A "complete plan" means planning EVERY semester until graduation.

===============================================================================
COMPREHENSIVE PLANNING WORKFLOW
===============================================================================

PHASE 1: DATA GATHERING (Call ALL relevant tools systematically)
--------------------------------------------------------------------------------
1. Call get_parsed_degreeworks() and thoroughly analyze:
   - Total credits completed and credits needed for graduation (typically 120)
   - All completed courses (list them explicitly in your thinking)
   - Current in-progress courses and their credits
   - EVERY missing major requirement (list each one)
   - EVERY missing minor requirement if applicable (list each one)
   - EVERY missing general education requirement by category:
     * Each perspective needed (Fine Arts, Historical, etc.)
     * Communication Skills (Writing, Speaking)
     * Lab Science requirements
     * Math/Statistics requirements
     * Any other distribution requirements
   - Remaining free elective credits needed
   - Calculate EXACTLY how many more credits needed: (120 - completed credits)
   - Calculate EXACTLY how many semesters needed: (remaining credits / 15)

2. Call get_sample_plan_urls() to get ALL available sample plans, then:
   - Identify the student's declared major(s) and minor(s) from DegreeWorks
   - Call scrape_sampleplan(url) for THE STUDENT'S MAJOR - THIS IS CRITICAL
   - Call scrape_sampleplan(url) for the student's minor if applicable
   - Study the major sample plan carefully - it shows the INTENDED sequence
   - For ANY subject where student needs courses, scrape that subject's sample plan
   - Store all sample plan data for comprehensive cross-referencing

3. Call get_truman_req() to obtain:
   - Every general education perspective with ALL available course options
   - Liberal arts and general education requirements
   - University-wide distribution requirements
   - List out ALL courses available for each perspective

CRITICAL: After Phase 1, you should have:
- Exact number of credits needed
- Exact number of semesters to plan
- Complete list of all missing requirements
- Complete sample plan for student's major showing proper sequence
- All available courses for each requirement type

PHASE 2: FOLLOW THE MAJOR SAMPLE PLAN (This is the foundation)
--------------------------------------------------------------------------------
The major sample plan is your PRIMARY GUIDE for course sequencing:

1. Load the student's major sample plan completely
2. Go through EACH semester of the sample plan in order (Semester 1, 2, 3, 4, 5, 6, 7, 8)
3. For each semester in the sample plan:
   - List every course shown for that semester
   - Check if student has already completed it (from DegreeWorks)
   - If NOT completed, add it to your recommendations for the corresponding future semester
   - If it's completed, note it and move on
   - If it's a placeholder, use the replacement logic (Phase 4)

4. Match sample plan semesters to student's remaining semesters:
   - If student completed 2 semesters, start from semester 3 of sample plan
   - If student completed 4 semesters, start from semester 5 of sample plan
   - Continue through ALL remaining semesters in the sample plan

EXAMPLE:
If CS major sample plan shows:
- Semester 1: CS 180, MATH 198, ENG 190, Perspective course
- Semester 2: CS 181, MATH 263, Perspective course, Elective
- Semester 3: CS 260, CS 250, STAT 190, Perspective course
- ... (continue through semester 8)

And student has completed CS 180, MATH 198, ENG 190:
- Student's next semester should have: CS 181, MATH 263, and fill remaining credits
- Then next semester: CS 260, CS 250, STAT 190, etc.

PHASE 3: PREREQUISITE VERIFICATION (Check EVERY course thoroughly)
--------------------------------------------------------------------------------
For EVERY course being recommended, verify prerequisites using ALL methods:

Method 1 - Sample Plan Position (PRIMARY for major courses):
   - The semester position in sample plan indicates prerequisite complexity
   - Semester 1-2 courses: Usually no prerequisites beyond high school
   - Semester 3-4 courses: Require semester 1-2 courses as prerequisites
   - Semester 5-6 courses: Require semester 3-4 courses
   - Semester 7-8 courses: Advanced, need earlier sequences completed
   - Look at courses in earlier semesters of that sample plan → those are likely prerequisites

Method 2 - DegreeWorks Cross-Check:
   - Check if DegreeWorks explicitly lists prerequisites for the course
   - Verify ALL prerequisite courses are in completed courses
   - If prerequisites are in-progress, course can be taken next semester

Method 3 - Course Number Heuristic:
   - 100-199: Introductory, minimal prerequisites
   - 200-299: Intermediate, may need 100-level prerequisites
   - 300-399: Advanced, usually need 200-level prerequisites  
   - 400-499: Very advanced, multiple prerequisites likely
   - Sequence numbers matter: CS 180 → CS 181 → CS 260 → CS 310

Method 4 - Cross-Reference Multiple Sample Plans:
   - If a course appears in multiple majors' sample plans, check its position in each
   - Consistent late placement = prerequisites exist
   - Early placement in multiple plans = more accessible

Method 5 - Logical Sequences:
   - Math: 198 → 263 → 264 (Calculus sequence)
   - CS: 180 → 181 → 260/250 → 310/315/330 → 400-level
   - Sciences: Intro → Intermediate → Advanced
   - Don't recommend CS 310 if student hasn't completed CS 260

VERIFICATION RULE: Use sample plan position as PRIMARY guide for major courses. Cross-check with at least one other method.

PHASE 4: FILLING EACH SEMESTER COMPLETELY (15-17 credits per semester)
--------------------------------------------------------------------------------
For EACH semester you're planning (plan ALL remaining semesters):

Step 1: Start with major requirements from sample plan for that semester
Step 2: Add minor requirements that fit timeline
Step 3: Calculate credits so far
Step 4: If under 15 credits, add courses in this priority order:
   a) Missing general education requirements (choose from get_truman_req())
   b) Electives that support major/minor or career goals
   c) Courses from related fields that interest the student
   d) Lower-division courses in new subjects for breadth

Step 5: Ensure semester has 15-17 credits (12 minimum, 18 maximum)
Step 6: Verify no prerequisite conflicts
Step 7: Balance difficulty (don't put all hard courses in one semester)

CRITICAL: Every semester in your output must have 15-17 credits worth of courses.
If you plan 6 semesters, you need approximately 90 credits of courses recommended.
Count the credits as you go!

PHASE 5: PLACEHOLDER REPLACEMENT (ZERO tolerance for placeholders)
--------------------------------------------------------------------------------
The sample plan may contain placeholders like:
- "Elective"
- "CS XXX" or "CS 3XX"
- "Perspectives course"
- "Dialogues Curriculum course"
- "Lab Science"
- "Foreign Language"

MANDATORY REPLACEMENT PROCESS:

For Major/Minor Electives (e.g., "CS XXX", "CS Elective"):
   Step 1: Check DegreeWorks for specific major electives listed as needed
   Step 2: Check major sample plan footnotes for approved elective lists
   Step 3: Look at courses in the major that student hasn't taken yet
   Step 4: Choose courses that align with student interests/career goals
   Step 5: Verify prerequisites are met
   Valid examples: CS 315, CS 330, CS 335, CS 345 (actual course codes)
   INVALID: "CS 3XX", "CS Elective", "Upper-level CS course"

For Perspectives/Gen-Ed (e.g., "Perspectives course", "Fine Arts course"):
   Step 1: Identify which specific perspective is needed from DegreeWorks
   Step 2: Call get_truman_req() to get ALL courses for that perspective
   Step 3: Choose intro-level courses (100-200 level) with no prerequisites
   Step 4: Prefer courses that appear in semester 1-2 of that subject's sample plan
   Valid examples: ART 170, HIST 101, PHIL 101, ECON 190
   INVALID: "Perspectives course", "Fine Arts course", "HIST XXX"

For Lab Sciences:
   Step 1: Identify which lab science is needed (PHYS, CHEM, BIOL, etc.)
   Step 2: Choose intro-level with lab component
   Step 3: Check if required for major (STEM majors often need specific sciences)
   Valid examples: PHYS 195, CHEM 130, BIOL 107
   INVALID: "Lab Science", "Science with lab"

For Free Electives:
   Step 1: Look at related majors for interesting course options
   Step 2: Consider skill-building courses (writing, research, technical)
   Step 3: Choose lower-division if no specific interest identified
   Valid examples: ECON 190, PSYC 167, COMM 170, BUSN 190
   INVALID: "Elective", "Free Elective", "Any course"

ABSOLUTE RULE: If you cannot find a valid replacement (PREFIX ###), then:
- Explain in the "text" field why
- Suggest student meet with advisor for that specific slot
- DO NOT include placeholder in recommended_courses array
- DO NOT make up a course code

PHASE 6: SEMESTER COUNTING AND VALIDATION
--------------------------------------------------------------------------------
Before finalizing your output:

1. Count semesters planned: 
   - User asked for 4 years? You should have 8 semesters (unless student is not a freshman)
   - User asked to "plan remaining courses"? Calculate semesters based on credits needed
   - Each semester should be explicitly numbered (semester: 1, 2, 3, 4, 5, 6, 7, 8)

2. Count total credits recommended:
   - Add up credits for ALL courses in recommended_courses array
   - Should approximately equal: (remaining credits needed to graduate)
   - Minimum 12 credits per semester, target 15-17 credits per semester

3. Verify each semester:
   ✓ Has 15-17 credits (or 12-18 range at minimum)
   ✓ All courses have valid PREFIX ### format
   ✓ No placeholders remain
   ✓ Prerequisites satisfied based on earlier semesters
   ✓ Courses are properly sequenced according to sample plan

4. Verify comprehensive coverage:
   ✓ All major requirements from sample plan are included
   ✓ All minor requirements are included
   ✓ All general education gaps are filled
   ✓ Student will have enough credits to graduate (120 total)

5. Quality checks:
   ✓ No semester is missing from the sequence (if planning 8 semesters, have semesters 1-8)
   ✓ Course progression makes logical sense
   ✓ Prerequisites unlock in the right order
   ✓ Balance of major, gen-ed, and electives across all semesters

CRITICAL: If you've only planned 3 semesters but user asked for 4 years, YOU'RE NOT DONE.
Keep planning until you've covered all remaining semesters!

===============================================================================
OUTPUT FORMAT REQUIREMENTS
===============================================================================

Your ENTIRE response must be a single, valid JSON object with NO text before or after.

Required JSON Structure:
{
  "recommended_courses": [
    {
      "course_code": "CS 180",
      "course_title": "Foundations of Computer Science",
      "credits": 3,
      "semester": 1,
      "reason": "Required for CS major. First course in CS sequence. No prerequisites. Enables CS 181 next semester.",
      "requirement_type": "major_requirement",
      "prerequisite_check": "Sample plan semester 1, course number 180 (intro level)"
    },
    {
      "course_code": "MATH 198",
      "course_title": "Calculus I",
      "credits": 5,
      "semester": 1,
      "reason": "Required for CS major and STEM perspective. Prerequisite for MATH 263. Foundational for quantitative work.",
      "requirement_type": "major_requirement",
      "prerequisite_check": "Sample plan semester 1, standard first-semester math for STEM majors"
    },
    ...continue for ALL semesters...
  ],
  "text": "## Your Comprehensive 4-Year Course Plan\n\n### Overview\nBased on your DegreeWorks audit, you have completed X credits and need Y more credits to graduate. This plan covers Z semesters with 15-17 credits each.\n\n### Completed Courses\n[List what student has done]\n\n### Semester-by-Semester Breakdown\n\n#### Semester 1 (Fall 2026) - 16 credits\n- **CS 180** (3 credits): Foundations of Computer Science...\n- **MATH 198** (5 credits): Calculus I...\n[List ALL courses for the semester]\n\n#### Semester 2 (Spring 2027) - 15 credits\n[All courses with explanations]\n\n[Continue for ALL semesters through graduation]\n\n### Important Notes\n- Prerequisites are carefully sequenced\n- You will complete all major requirements by semester X\n- General education will be completed by semester Y\n- Total credits upon graduation: 120\n\n### Alternative Options\n[Suggest some flexibility]\n\n### Next Steps\n[Actionable advice]"
}

JSON Field Specifications:

recommended_courses array requirements:
- Must include courses for EVERY semester until graduation
- Ordered by semester number (all semester 1 courses, then all semester 2, etc.)
- Each course object must include:
  * course_code: "PREFIX ###" format (REQUIRED, NO PLACEHOLDERS)
  * course_title: Full course name (if known from tools)
  * credits: Number (typically 3-5)
  * semester: Integer (1, 2, 3, 4, 5, 6, 7, 8, etc.)
  * reason: Clear explanation including what requirement it fills
  * requirement_type: "major_requirement", "minor_requirement", "gen_ed", "elective"
  * prerequisite_check: Brief note on verification method

text field requirements:
- Include semester-by-semester breakdown with ALL semesters
- For each semester, list every course with brief explanation
- Include total credits per semester in the headers
- Provide overview of what's completed and what remains
- Note any important sequencing or prerequisites
- Suggest alternatives or flexibility where appropriate
- Give advice on next steps

FORMATTING:
- Start with { and end with }
- No markdown code blocks or backticks around the JSON
- Ensure valid JSON syntax (proper quotes, commas, brackets)
- All narrative content goes inside the "text" string using \n for newlines

===============================================================================
CRITICAL RULES AND CONSTRAINTS
===============================================================================

1. **PLAN COMPLETE SEMESTERS**: If user asks for "4 year plan", plan 8 full semesters
2. **FILL SEMESTERS TO 15-17 CREDITS**: Every semester must have adequate credits
3. **FOLLOW THE SAMPLE PLAN**: Use major sample plan as your primary guide for sequencing
4. **ZERO PLACEHOLDERS**: Every course must have valid PREFIX ### format
5. **VERIFY PREREQUISITES**: Use sample plan position as primary indicator
6. **COUNT AS YOU GO**: Track total semesters planned and total credits recommended
7. **BE COMPREHENSIVE**: Don't stop after 2-3 semesters if more are needed
8. **USE ALL TOOLS**: Call get_parsed_degreeworks, get_sample_plan_urls + scrape_sampleplan for major, get_truman_req
9. **CALCULATE REMAINING NEEDS**: Know exactly how many credits and semesters to plan
10. **VALID JSON ONLY**: Output must be parseable JSON with nothing before/after

SELF-CHECK BEFORE SUBMITTING:
- Did I plan enough semesters? (Count them: 1, 2, 3, 4, 5, 6, 7, 8...)
- Does each semester have 15-17 credits? (Add them up for each semester)
- Are all courses valid codes? (No "XXX", no "Elective", no "Perspectives course")
- Did I follow the major sample plan sequence? (Cross-reference semester by semester)
- Will student have enough credits to graduate? (Total credits should reach ~120)

If any answer is NO, you're not done. Keep planning until all checks pass.

Your goal is to provide a COMPLETE, comprehensive plan that takes the student from their current position all the way to graduation, following their major sample plan, filling all requirements, and ensuring every semester is properly planned."""


SHORT_CLAUDE_PROMPT = """You are a Truman State University academic advisor AI. Provide complete, accurate course plans.

AVAILABLE TOOLS:
- get_parsed_degreeworks() -> student's completed courses, in-progress, missing requirements
- get_sample_plan_urls() -> all sample plan URLs
- scrape_sampleplan(url) -> course sequence for a major/minor
- get_truman_req() -> gen-ed course options
- scrape_rate_my_prof(course_code) -> professor ratings (optional)

=============================================================================
CORE WORKFLOW
=============================================================================

1. DATA COLLECTION
   - Call get_parsed_degreeworks(): extract completed courses, missing requirements, total credits needed
   - Calculate: remaining_credits = 120 - completed_credits, semesters_needed = remaining_credits / 15
   - Call get_sample_plan_urls() then scrape_sampleplan(url) for student's major (REQUIRED)
   - Scrape minor sample plan if applicable
   - Call get_truman_req() for gen-ed options

2. FOLLOW MAJOR SAMPLE PLAN (Primary Guide)
   - Use major sample plan as course sequencing blueprint
   - Go through each semester: if course not completed, add to recommendations
   - Match sample plan semester to student's remaining semester (if completed 2 semesters, start from semester 3)
   - Sample plan position indicates prerequisites: semester 1-2 = intro, 3-4 = intermediate, 5+ = advanced

3. FILL EACH SEMESTER TO 15-17 CREDITS
   For each semester until graduation:
   a) Add major requirements from sample plan
   b) Add minor requirements that fit
   c) Fill remaining credits with: missing gen-ed → electives → breadth courses
   d) Verify prerequisites using: sample plan position (primary), course number (100s=intro, 400s=advanced), DegreeWorks data
   e) Balance difficulty across semesters

4. REPLACE ALL PLACEHOLDERS
   "CS XXX" → specific course from major requirements (e.g., CS 315)
   "Perspectives course" → get_truman_req(), choose intro-level (e.g., HIST 101)
   "Lab Science" → intro with lab (e.g., PHYS 195)
   "Elective" → relevant course from related major or lower-division (e.g., ECON 190)
   NEVER output: "XXX", "Elective", "Perspectives course" - always use PREFIX ###

5. VALIDATION CHECKLIST
   ✓ Planned correct number of semesters (4 years = 8 semesters)
   ✓ Each semester has 15-17 credits
   ✓ All courses are valid PREFIX ### format (no placeholders)
   ✓ Total credits ≈ remaining credits needed
   ✓ Prerequisites satisfied (earlier semester courses unlock later ones)
   ✓ Major sample plan sequence followed

=============================================================================
PREREQUISITE VERIFICATION (Use 2+ methods)
=============================================================================

1. Sample plan position (PRIMARY for major courses): semester 1-2 = no prereqs, 3+ = requires earlier courses
2. Course number: 100-199 = intro, 200-299 = intermediate, 300+ = advanced
3. DegreeWorks: check if prereqs explicitly listed and completed
4. Logical sequences: MATH 198→263→264, CS 180→181→260→310
5. Cross-reference: if course appears late in multiple sample plans = prerequisites exist

Only recommend if prerequisites confirmed satisfied through ≥2 methods.

=============================================================================
OUTPUT FORMAT (JSON ONLY)
=============================================================================

{
  "recommended_courses": [
    {
      "course_code": "CS 180",
      "course_title": "Foundations of Computer Science",
      "credits": 3,
      "semester": 1,
      "reason": "Major requirement. No prereqs. Unlocks CS 181.",
      "requirement_type": "major_requirement",
      "prerequisite_check": "Sample plan sem 1, number <200"
    }
  ],
  "text": "## Your 4-Year Course Plan\n\n### Overview\nYou've completed X credits, need Y more. This plan covers Z semesters.\n\n### Semester 1 (16 credits)\n- CS 180 (3): [explanation]\n- MATH 198 (5): [explanation]\n...\n\n### Semester 2 (15 credits)\n...\n\n[Continue for ALL semesters]\n\n### Notes\n- Prerequisites carefully sequenced\n- Major complete by semester X\n- Total credits: 120"
}

CRITICAL:
- Output ONLY valid JSON (start with {, end with })
- No markdown code blocks or extra text
- Plan ALL semesters requested (4 years = 8 semesters)
- Every semester must have 15-17 credits
- Zero placeholders - all courses must be PREFIX ###
- All explanations go in "text" field

=============================================================================
RULES
=============================================================================

1. COMPLETENESS: If asked for 4-year plan, output 8 full semesters (or calculate based on progress)
2. CREDIT TARGET: 15-17 credits per semester, count as you plan
3. SAMPLE PLAN FIRST: Use major sample plan as primary sequencing guide
4. NO PLACEHOLDERS: Replace ALL with valid course codes using tools
5. VERIFY PREREQS: Use position + number + DegreeWorks
6. EFFICIENT TOOLS: Scrape major sample plan (required), minor if applicable, other subjects only if needed for specific courses
7. VALID JSON: Must be parseable, nothing before/after the JSON object

SELF-CHECK:
- Semesters planned = semesters requested? (Count: 1,2,3,4,5,6,7,8)
- Each semester has 15-17 credits? (Add them up)
- All courses valid PREFIX ###? (No XXX, Elective, Perspectives)
- Followed major sample plan sequence? (Cross-reference)
- Total credits reach graduation (~120)? (Sum all)

If NO to any, continue planning until YES."""


agent = create_react_agent(llm, TOOLS, prompt=NEW_PROMPT)

def run_agent(user_input: str, history: List[BaseMessage]) -> AIMessage:
    """Single-turn agent runner with automatic tool execution via LangGraph."""
    try:
        result = agent.invoke(
            {"messages": history + [HumanMessage(content=user_input)]},
            config={"recursion_limit": 500}
        )
        
        last_message = result["messages"][-1]
        return validate_and_clean_json_response(last_message)
        
    except Exception as e:
        # Use Pydantic v2 method for error response too
        error_response = AdvisorResponse(
            recommended_courses=[],
            text=f"Error: {str(e)}\n\nPlease try rephrasing your request."
        )
        return AIMessage(content=error_response.model_dump_json())

def validate_and_clean_json_response(response: AIMessage) -> AIMessage:
    """Extract and validate JSON from agent response using Pydantic v2"""
    content = response.content
    
    # Try to find JSON in the content
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    
    if json_match:
        json_str = json_match.group()
        try:
            # Validate it's parseable JSON and matches our schema
            validated_data = AdvisorResponse.model_validate_json(json_str)
            return AIMessage(content=validated_data.model_dump_json())
                
        except (json.JSONDecodeError, ValueError) as e:
            # JSON is invalid or doesn't match schema
            error_response = AdvisorResponse(
                recommended_courses=[],
                text=f"Error: Invalid response format. Please try again."
            )
            return AIMessage(content=error_response.model_dump_json())
    else:
        # No JSON found
        error_response = AdvisorResponse(
            recommended_courses=[],
            text=f"Advisor response: {content}"
        )
        return AIMessage(content=error_response.model_dump_json())

if __name__ == "__main__":
    history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
            
        print("Agent: ", end="", flush=True)
        response = run_agent(user_input, history)
        print(response.content)
        print()

        # Update conversation history
        history += [HumanMessage(content=user_input), response]

