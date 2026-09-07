import json
import os

data = {
  "museum": {
    "history": [
      {
        "claim": "Takua Pa Community Museum is a two-story building inside Wat Sena Nucharangsan. It collects utensils and equipment reflecting the local way of life, including items from the tin mining era.",
        "quote": "Takua Pa Community Museum is a two-story building"
      },
      {
        "claim": "Wat Sena Nucharangsan was built by Phraya Senanuchit (Nuch) and its ordination hall (ubosot) has Chinese architectural influence.",
        "quote": "Built by Phraya Senanuchit (Nuch)"
      },
      {
        "claim": "Wat Sena Nucharangsan's registration record indicates its establishment in 1847 (2390 BE).",
        "quote": "Establishment date 2390"
      },
      {
        "claim": "The temple's ordination hall was registered as an ancient monument by the Fine Arts Department, but the reviewed sources do not specify the year.",
        "quote": "Registered by the Fine Arts Department"
      }
    ],
    "timeline": [
      {
        "title": "Establishment of Wat Sena Nucharangsan",
        "detail": "Temple records state it was established in 1847 (2390 BE); local sources identify Phraya Senanuchit (Nuch) as the founder."
      },
      {
        "title": "Part of old town tourism context",
        "detail": "Takua Pa Community Museum is mentioned as part of the old town cultural street, but no specific opening hours are announced."
      },
      {
        "title": "Ordination hall registered as an ancient monument",
        "detail": "The Fine Arts Department registered the ordination hall, but the reviewed sources do not specify the year."
      },
      {
        "title": "Community museum established in a two-story building",
        "detail": "Academic sources describe the building and exhibits, but the establishment year and founder are not found."
      }
    ],
    "news": [
      {
        "title": "Phang Nga hosts the 12th 'From Takola to Takua Pa' event",
        "summary": "The event promotes Takua Pa old town tourism, linking to local lifestyle learning and community economy, but the news does not directly confirm activities inside the museum."
      },
      {
        "title": "Tracing the legend of Takola to the charm of Takua Pa old town",
        "summary": "Phang Nga province and the municipality promote old town tourism and stimulate the community economy. No specific mention of museum restoration."
      }
    ],
    "nearby": [
      {
        "name": "Sin Chai Tung Shrine"
      },
      {
        "name": "Ku Chai Tung Shrine"
      },
      {
        "name": "Khun In House"
      },
      {
        "name": "Takua Pa Governor's Residence Wall"
      }
    ],
    "visit": {
      "best_time": "Sunday evenings are suitable for continuing a trip on the Takua Pa old town cultural street.",
      "parking": None,
      "wheelchair": None,
      "dress_code": "Modest attire is recommended when entering the temple grounds.",
      "opening_hours": None,
      "admission_fee": None
    },
    "address_line": "Inside Wat Sena Nucharangsan, old market area"
  },
  "guan-yu": {
    "history": [
      {
        "claim": "The municipality states that the shrine originated from the faith of Hokkien Chinese in Takua Pa, is over a century old, and serves as a spiritual anchor through the belief in Guan Yu and Guanyin.",
        "quote": "Originated from the faith of Hokkien Chinese"
      },
      {
        "claim": "The municipality identifies this shrine as the origin of the Takua Pa vegetarian festival.",
        "quote": "The origin of the Takua Pa vegetarian festival"
      },
      {
        "claim": "Gplace website presents a story that a tin smelter owner in Khlong Pi community named Lim Bun Tuek founded the Guan Yu shrine and started the vegetarian festival in 1843 (2386 BE); the spelling of the name is inconsistent and there is no primary evidence to verify this.",
        "quote": "Hypothesis of the start of the vegetarian festival"
      },
      {
        "claim": "A story on Gplace states that Lim Eng Cheng, or Taokae Pho Daeng, raised funds to buy a house to permanently relocate the shrine in 1902 (2445 BE); the construction year of the building is not verified.",
        "quote": "In 2445"
      },
      {
        "claim": "Gplace categorizes the shrine building as Sino-Portuguese and notes there is another Chinese shrine building across the street.",
        "quote": "Sino-Portuguese style building"
      },
      {
        "claim": "News on October 2, 2024 (2567 BE) records the Go Teng pole raising ceremony at Rong Phra Talat Tai to start the vegetarian festival.",
        "quote": "Go Teng pole raising ceremony"
      }
    ],
    "timeline": [
      {
        "title": "Story of the shrine's founding and the start of the vegetarian festival",
        "detail": "Gplace states that the Guan Yu shrine was founded and the 9-day vegetarian festival started in the Khlong Pi community, but there is no primary evidence to verify this."
      },
      {
        "title": "Story of permanent relocation to Talat Yai",
        "detail": "Gplace notes fundraising to buy a house to relocate the shrine to Talat Yai, but it is not verified if this was the year the current building was constructed."
      },
      {
        "title": "Go Teng pole raising at Rong Phra Talat Tai",
        "detail": "News reports the Go Teng pole raising ceremony to start the Takua Pa people's vegetarian festival."
      }
    ],
    "news": [
      {
        "title": "An old shrine in Takua Pa district, Phang Nga province, has performed the Go Teng pole raising ceremony",
        "summary": "Reports on the Go Teng pole raising ceremony at Guan Yu (Sin Chai Tung) Shrine, Rong Phra Talat Tai, to begin the vegetarian festival."
      }
    ],
    "nearby": [
      {
        "name": "Old Town Wall"
      },
      {
        "name": "Wat Na Mueang"
      },
      {
        "name": "Ku Chai Tung Shrine"
      },
      {
        "name": "Wat Sena Nucharangsan"
      }
    ],
    "visit": {
      "best_time": "The vegetarian festival is a suitable time to observe community rituals. The schedule must be checked for the year of travel; 2024 news indicated October 2-11, which is not the 2026 schedule.",
      "parking": None,
      "wheelchair": None,
      "dress_code": "Community sources note that vegetarian festival participants wear white; no dress code requirements are found for normal days.",
      "opening_hours": None,
      "admission_fee": None
    },
    "address_line": "Around the intersection of Udom Thara Road and Si Takua Pa Road, Talat Yai area, Takua Pa Subdistrict, Takua Pa District, Phang Nga Province"
  },
  "pun-thao": {
    "history": [
      {
        "claim": "Municipal documents state that Pun Thao Kong Am Shrine is the first shrine of Takua Pa town, located in the old port area called Chap Se.",
        "quote": "The first shrine of Takua Pa town"
      },
      {
        "claim": "The founders were Chinese immigrants who came to mine tin in Takua Pa. Sources mention Hokkien, Hainanese, and Cantonese groups, but do not specify individual names or the construction year.",
        "quote": "Built by Chinese immigrants who came to mine tin"
      },
      {
        "claim": "The municipality records that inside the shrine is an incense burner bestowed by King Rama VI, though the year or occasion is not specified.",
        "quote": "Inside the shrine is an incense burner bestowed by King Rama VI"
      },
      {
        "claim": "A travel article identifies the deity Pun Thao Kong as the principal god, noting beliefs about community protection and prosperity in trade.",
        "quote": "Has the deity Pun Thao Kong as the principal god"
      }
    ],
    "timeline": [
      {
        "title": "Birthday ceremony and faith activities at the shrine",
        "detail": "There is a video recording the birthday ceremony of Hok Tek Chia Sin / Pae Kong at Pun Thao Kong Am Shrine, Chap Se."
      },
      {
        "title": "Oil bathing ceremony, Phra La, and inviting the sacred fire",
        "detail": "Another video mentions the shrine's rituals and the return of Takua Pa descendants to join the event."
      },
      {
        "title": "Start of shrine construction",
        "detail": "The construction year and founder's name are not yet found; official sources identify it as the first shrine in Takua Pa town."
      },
      {
        "title": "Incense burner bestowed by King Rama VI",
        "detail": "The municipality states there is an incense burner bestowed by King Rama VI, but does not specify the year or occasion."
      }
    ],
    "news": [
      {
        "title": "Birthday of Hok Tek Chia Sin (Pae Kong), Pun Thao Kong Am Shrine, Chap Se, Takua Pa town",
        "summary": "A news video/recording of the shrine's birthday ceremony activities."
      }
    ],
    "nearby": [
      {
        "name": "Chap Se area shophouses, Udom Thara Road"
      },
      {
        "name": "Old town wall camp, Udom Thara Road"
      }
    ],
    "visit": {
      "best_time": None,
      "parking": None,
      "wheelchair": None,
      "dress_code": None,
      "opening_hours": None,
      "admission_fee": None
    },
    "address_line": "Udom Thara Road, Talat Yai community, Takua Pa Subdistrict, Takua Pa District, Phang Nga Province"
  }
}

os.makedirs(r'D:\Siwaracafeweb\output\web\takuapa101-v1\data\i18n\en\details', exist_ok=True)
with open(r'D:\Siwaracafeweb\output\web\takuapa101-v1\data\i18n\en\details\det-03.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Done")
