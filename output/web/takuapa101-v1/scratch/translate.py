import json
import os

data = {
  "siwara-cafe": {
    "name": "Siwara Cafe",
    "one_liner": "A cafe in Takua Pa and the creator of this town guide."
  },
  "baan-bai": {
    "name": "Baan Bai",
    "one_liner": ""
  },
  "pa-daeng-khanom-wan": {
    "name": "Pa Daeng Khanom Wan",
    "one_liner": "Traditional Thai dessert shop with rich flavors and friendly prices in the Lan Long market area."
  },
  "khanom-jeen-pa-mom": {
    "name": "Khanom Jeen Pa Mom",
    "one_liner": "A long-standing Khanom Jeen (rice noodles) shop in Takua Pa, offering 8 types of curries and a full set of fresh side vegetables."
  },
  "khanom-jeen-phi-neng": {
    "name": "Khanom Jeen Phi Neng",
    "one_liner": "Flavorful Khanom Jeen (rice noodles) in the Lan Long market with unlimited fresh and pickled vegetables at affordable prices."
  },
  "khanom-jeen-nai-na": {
    "name": "Khanom Jeen Nai Na",
    "one_liner": "Khanom Jeen (rice noodles) shop in a shady palm garden setting, served as a set with various curries."
  },
  "mata-coffee-and-bakery": {
    "name": "Mata Coffee And Bakery",
    "one_liner": "A relaxed coffee and bakery shop known for its freshly baked homemade cakes."
  },
  "the-eighth-room": {
    "name": "The Eighth Room",
    "one_liner": "Loft-style cafe in the Khao Lak area offering savory dishes, desserts, and matcha green tea."
  },
  "delicacy-khaolak": {
    "name": "Delicacy Khaolak",
    "one_liner": "Bali-style cafe and bakery featuring homemade pastries and a warm atmosphere."
  },
  "garang-khao-lak": {
    "name": "Garang Khao Lak",
    "one_liner": "A cafe with modern design, known for its homemade ice cream with over a hundred flavors to choose from."
  },
  "baan-khanom-arom-dee": {
    "name": "Baan Khanom Arom Dee",
    "one_liner": "Minimalist cafe offering soft cakes and custom made-to-order cakes for special occasions."
  },
  "ocean-man-cafe": {
    "name": "Ocean Man Café",
    "one_liner": "Minimalist red brick cafe shaped like a wave, offering homemade bakery items and an outdoor pet-friendly zone."
  },
  "la-malila-cafe": {
    "name": "La Malila Café",
    "one_liner": "Elegant cafe in the Bang Niang beach area featuring house-roasted coffee and freshly baked goods."
  },
  "pa-fon-khanom-wan": {
    "name": "Pa Fon Khanom Wan",
    "one_liner": "Local Thai dessert shop offering a variety of menu items located in Jae Mook market."
  },
  "the-eighth-room-by-mata-cafe": {
    "name": "The Eighth Room by mata cafe",
    "one_liner": "Cozy cafe in the Khao Lak area serving brunch, homemade waffles, and a variety of drinks."
  },
  "garang-artisan-icecream": {
    "name": "Garang Artisan Icecream",
    "one_liner": "Homemade ice cream shop and cafe by Bang Sak beach featuring Moroccan-style decoration and ice cream flavors made with local ingredients."
  },
  "yellow-snail-cafe-gallery": {
    "name": "Yellow Snail Cafe & Gallery",
    "one_liner": "Bare concrete style cafe in the Khao Lak area, notable for its coffee and art exhibitions."
  },
  "mahamitr-cafe": {
    "name": "Mahamitr Cafe",
    "one_liner": "Dark minimalist cafe set in a shady palm garden, featuring a surf skate park and single-dish meals."
  },
  "trok-ca-fe": {
    "name": "TROK CA'FE",
    "one_liner": "A vintage coffee shop located in an alley of Takua Pa Old Town, offering a raw, cool atmosphere among century-old ruins."
  },
  "tribe-khaolak": {
    "name": "Tribe.Khaolak",
    "one_liner": "Homely, pet-friendly cafe and brunch spot with a warm atmosphere that turns into a bar in the evening."
  },
  "valhalla-villas-teahouse": {
    "name": "Valhalla Villas & Teahouse",
    "one_liner": "Minimalist cafe on a Khao Lak hill, featuring large windows offering panoramic views of the Andaman Sea."
  },
  "karkinos-khao-lak": {
    "name": "KARKINOS KHAO LAK",
    "one_liner": "Beach club and Italian restaurant at Pakarang beach with an open-air atmosphere suitable for watching the sunset."
  },
  "underground-tea-cafe": {
    "name": "Underground Tea Cafe",
    "one_liner": "Loft-style bubble tea cafe located in the basement of a noodle shop in the old town area."
  },
  "unnamed-khaolak": {
    "name": "Unnamed Khaolak",
    "one_liner": "Homey cafe in a white house styled like a surf club, serving brunch and freshly roasted coffee."
  },
  "tubtim-dimsum": {
    "name": "Tubtim Dimsum",
    "one_liner": "Breakfast and dim sum shop with a good atmosphere, surrounded by a flower garden and shady trees."
  },
  "kai-tong-dimsum": {
    "name": "Kai Tong Dimsum",
    "one_liner": "Freshly steamed dim sum and breakfast shop frequented by locals and tourists."
  },
  "punthong-dimsum": {
    "name": "Punthong Dimsum",
    "one_liner": "Dim sum shop offering over 60 freshly steamed menus where customers can choose from the cabinet for quick, hot service."
  },
  "hua-ta-bistro": {
    "name": "Hua Ta Bistro",
    "one_liner": "Fusion restaurant in an old house, decorated in a vintage Takua Pa retro style."
  },
  "ice-tae-cha-chak": {
    "name": "Ice Tae Cha Chak",
    "one_liner": "Halal restaurant and evening drink shop known for its pulled tea performance and volcano roti."
  },
  "lert-ocha": {
    "name": "Lert Ocha",
    "one_liner": "Traditional Kopitiam (coffee shop) style breakfast place in Takua Pa, offering a glimpse of the traditional way of life."
  },
  "krua-luang-ten": {
    "name": "Krua Luang Ten",
    "one_liner": "A Michelin Guide-featured Southern Thai restaurant with intense flavors, self-described as the most delicious in the human world."
  },
  "khrua-nong": {
    "name": "Khrua Nong",
    "one_liner": "Mini-sized Southern Thai restaurant featured in the Michelin Guide, offering dishes such as stir-fried Baegu leaves with egg and dried shrimp."
  },
  "yim-yim-restaurant": {
    "name": "Yim Yim Restaurant",
    "one_liner": "Local restaurant open for over 30 years, blending Chinese and Southern Thai cuisines."
  },
  "timbre": {
    "name": "Timbre",
    "one_liner": "Restaurant and bar with a good atmosphere and live music, suitable for relaxing at night."
  },
  "khrua-ko-yot": {
    "name": "Khrua Ko Yot",
    "one_liner": "Southern Thai and made-to-order restaurant with intense flavors and friendly prices."
  },
  "khonkon-kitchen": {
    "name": "Khonkon Kitchen",
    "one_liner": "Family-style Southern Thai local restaurant with comfortable bamboo pavilion seating."
  },
  "karkinos-khaolak": {
    "name": "KARKINOS Khaolak",
    "one_liner": "Beach club and Italian restaurant at Pakarang beach, offering a chill atmosphere for watching the sunset."
  },
  "the-eighth-room-by-mata-cafe-2": {
    "name": "The Eighth Room by mata cafe",
    "one_liner": "Cozy cafe along the Khao Lak road with a warm atmosphere, offering all-day breakfast and homemade desserts."
  },
  "swell-cafe": {
    "name": "Swell Cafe",
    "one_liner": "Homey cafe capturing the sea breeze, child-friendly with toys available for play."
  },
  "cotton-cafe-and-library": {
    "name": "Cotton Cafe and Library",
    "one_liner": "Library-style cafe in a hotel overlooking the swimming pool."
  },
  "jee-tarn-souvenir-shop": {
    "name": "Jee Tarn Souvenir Shop",
    "one_liner": "A center for Phang Nga's OTOP (One Tambon One Product) goods with a comprehensive range of souvenirs."
  },
  "shop": {
    "name": "Natchawal Shop",
    "one_liner": "Souvenir shop in the Takua Pa bus terminal area, a hub for local snacks and OTOP products."
  },
  "kongsri-souvenir-shop": {
    "name": "Kongsri Souvenir Shop",
    "one_liner": "Takua Pa local snack and souvenir shop focusing on fresh baking and beautiful packaging."
  },
  "shop-2": {
    "name": "Yiam Tian Heng (Ko Yiam)",
    "one_liner": "Original shop of the successors who make traditional Mua Lao (sesame puffs) in Takua Pa."
  },
  "siriporn-batik": {
    "name": "Siriporn Batik",
    "one_liner": "Batik painting and natural leaf printing shop featuring handmade crafts by locals."
  },
  "shop-3": {
    "name": "Pa Lan Traditional Khanom Buang",
    "one_liner": "Shop in Takua Pa fresh market selling traditional Khanom Buang (Thai crepes) made from their own milled rice flour."
  },
  "shop-4": {
    "name": "Batik Mudyom @Takua Pa (Chao Su Phan Phra)",
    "one_liner": "Batik and tie-dye art reflecting local identity by Takua Pa artists."
  },
  "eco-print-by-kanokwan": {
    "name": "Eco Print by Kanokwan",
    "one_liner": "A group of leaf print and batik fabric makers offering environmentally friendly products."
  },
  "shop-5": {
    "name": "Tamnan Kosui Am Nai Suan",
    "one_liner": "Traditional Kosui (sweet cup cake) recipe, sold only once a year during the vegetarian festival."
  }
}

os.makedirs('data/i18n/en', exist_ok=True)
with open('data/i18n/en/shops.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(len(data))
