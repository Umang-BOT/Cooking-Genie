import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
import numpy as np
from collections import defaultdict
import streamlit as st
from PIL import Image
import base64
import io


# Define the path of the new background image file
new_background_image_path = "C:/Users/Umang/Downloads/pxfuel.jpg"

# Convert the new image file into a base64 encoded string
def get_base64_of_image(image_path):
    img = Image.open(image_path)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG") 
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Get the base64 string of the new image
new_image_base64 = get_base64_of_image(new_background_image_path)

# Set the new background image using CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background: url('data:image/png;base64,{new_image_base64}');
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

stop_words = set(stopwords.words('english'))

recipe_names = [
    "Butter Chicken",
    "Paneer Tikka",
    "Chole Bhature",
    "Chicken Biryani",
    "Dal Makhani",
    "Samosa",
    "Aloo Gobi",
    "Palak Paneer",
    "Pani Puri",
    "Rajma Chawal",
    "Gulab Jamun",
    "Vada Pav",
    "Pav Bhaji",
    "Chana Masala",
    "Masala Dosa",
    "Tandoori Chicken",
    "Chicken Curry",
    "Fish Curry",
    "Bhindi Masala",
    "Mutton Curry",
    "Kadai Paneer",
    "Dahi Puri",
    "Hyderabadi Biryani",
    "Dum Aloo",
    "Kheer",
    "Phirni",
    "Jalebi",
    "Aloo Paratha",
    "Gajar Ka Halwa",
    "Kulfi",
    "Chole Tikka Chaat",
    "Pakora",
    "Chicken Cafreal",
    "Kansar",
    "Modak",
    "Gulab Jamun",
    "Ras Malai",
    "Veg Biryani",
    "Shahi Paneer",
    "Kadhi Pakora",
    "Rasgulla",
    "Bebinca",
    "Kofta Curry",
    "Rogan Josh",
    "Shrikhand",
    "Aloo Tikki",
    "Chaat",
]

recipes = [
    "chicken, butter, onion, tomato, cream",
    "paneer, yogurt, spices",
    "chickpeas, flour, spices",
    "chicken, rice, spices",
    "black lentils, kidney beans, butter, cream",
    "potato, peas, spices",
    "potato, cauliflower, spices",
    "cottage cheese, spinach, spices",
    "puri, tamarind chutney, spicy water",
    "kidney beans, rice, spices",
    "milk, sugar, saffron",
    "potato, bun, chutney",
    "mashed vegetables, bun, spices",
    "chickpeas, spices",
    "fermented crepe, potato filling, spices",
    "marinated chicken, yogurt, spices",
    "chicken, spices, tomato",
    "fish, spices, tomato",
    "okra, spices",
    "goat meat, spices",
    "cottage cheese, spices",
    "puris, spicy water, tamarind chutney",
    "spiced wheat, ghee",
    "rice pudding, saffron, nuts",
    "ground rice, milk, sugar",
    "deep-fried sweets, sugar syrup",
    "potato, wheat bread, spices",
    "grated carrots, milk, sugar",
    "frozen dairy dessert, pistachios",
    "spiced chickpeas, chutneys",
    "deep-fried snack, gram flour",
    "spicy grilled chicken, Goan spices",
    "sweet wheat, ghee",
    "sweet rice dumplings, coconut",
    "fried balls, sugar syrup",
    "saffron milk, cottage cheese dumplings",
    "rice, meat, spices",
    "cottage cheese, gravy, spices",
    "yogurt-based gravy, chickpea flour dumplings",
    "sugar syrup-soaked sweets, nuts",
    "sweet rice, saffron",
    "red kidney beans, spices",
    "lamb, yogurt, spices",
    "sweet yogurt dessert, cardamom",
    "spiced potato patties",
    "fermented crepe, potato filling",
    "savory snack, chutneys",
]

description={
    "Butter Chicken":"Marinate the chicken with yogurt, ginger-garlic paste, salt, turmeric, and red chili powder for an hour. Heat oil in a pan and fry the chicken until golden. Remove and keep aside. In the same pan, add butter, onion, tomato, cashew nuts, salt, garam masala, fenugreek leaves, and water. Cook until soft and then blend into a smooth sauce. Return the sauce to the pan and bring to a boil. Add the chicken and cream and simmer for 15 minutes. Garnish with coriander leaves and serve hot with naan bread or rice.",
    "Paneer Tikka":"Cut the paneer into cubes and marinate with yogurt, ginger-garlic paste, salt, turmeric, red chili powder, coriander powder, cumin powder, garam masala, and lemon juice for an hour. Thread the paneer cubes onto skewers along with onion and capsicum pieces. Grill or bake in a preheated oven for 15 minutes, turning occasionally. Brush with melted butter and serve hot with mint chutney.",
    "Chole Bhature":"Soak the chickpeas overnight in water with a pinch of baking soda. Drain and pressure cook with salt, turmeric, tea bags, and water for 15 minutes or until soft. Discard the tea bags and keep the chickpeas aside. Heat oil in a pan and add cumin seeds, bay leaf, cinnamon stick, cloves, cardamom pods, and asafoetida. Fry for a minute and then add onion, ginger-garlic paste, green chilies, and salt. Cook until golden and then add tomato, red chili powder, coriander powder, cumin powder, garam masala, and amchur powder. Cook until the oil separates and then add the chickpeas and some water. Simmer for 10 minutes and then mash some of the chickpeas to thicken the gravy. Garnish with coriander leaves and serve hot with bhature. To make bhature, mix flour, yogurt, salt, sugar, baking powder, and oil in a bowl. Knead into a soft dough and let it rest for an hour. Divide the dough into equal balls and roll them into thin circles. Deep fry in hot oil until puffed and golden. Drain on paper towels and serve hot with chole.",
    "Chicken Biryani":"Marinate the chicken with yogurt, ginger-garlic paste, red chili powder, turmeric, garam masala, and salt for an hour. In a large pot, heat ghee and add whole spices like bay leaves, cinnamon, cardamom, and cloves. Add sliced onions and cook until golden. Add the marinated chicken and cook until it changes color. Layer the partially cooked rice over the chicken and add saffron milk, fried onions, and ghee. Cover the pot tightly and cook on low heat until the rice is fully cooked. Serve hot with raita.",
    "Dal Makhani":"Soak black lentils and kidney beans overnight in water. Drain and pressure cook with water, salt, and turmeric for 15 minutes or until soft. In a separate pan, heat ghee and add cumin seeds, bay leaf, and dried red chilies. Add chopped onions and cook until golden. Add ginger-garlic paste, green chilies, and tomatoes. Cook until the tomatoes are soft and then add red chili powder, coriander powder, and garam masala. Cook until the oil separates and then add the cooked lentils and beans. Simmer for 20-30 minutes on low heat, stirring occasionally. Add cream and butter and cook for another 5 minutes. Serve hot with naan or rice.",
    "Samosa":"For the filling, heat oil and add cumin seeds, fennel seeds, and ginger-garlic paste. Add boiled and mashed potatoes, green peas, and spices like coriander powder, cumin powder, garam masala, and amchur powder. Mix well and cook until the filling is dry. Allow it to cool. For the outer covering, mix flour, salt, and ajwain seeds. Add ghee and mix until the mixture resembles breadcrumbs. Add water and knead into a smooth dough. Divide the dough into small balls and roll them into thin circles. Cut each circle in half. Take one semicircle and fold it into a cone, sealing the edges with water. Fill the cone with the potato filling and seal the top. Deep fry the samosas until golden brown. Serve hot with green chutney and tamarind chutney.",
    "Aloo Gobi":"Heat oil in a pan and add cumin seeds and mustard seeds. Add chopped onions and cook until golden. Add ginger-garlic paste and green chilies. Cook for a minute and then add chopped cauliflower and potatoes. Stir well and add turmeric, red chili powder, cumin powder, coriander powder, and garam masala. Mix everything and cook on low heat until the vegetables are tender. Garnish with coriander leaves and serve hot with roti or rice.",
    "Palak Paneer":"Blanch spinach leaves in hot water and then blend into a smooth puree. In a pan, heat oil and add cumin seeds. Add chopped onions and cook until golden. Add ginger-garlic paste and cook for a minute. Add chopped tomatoes and cook until soft. Add turmeric, red chili powder, and garam masala. Cook until the oil separates. Add the spinach puree and cook for a few minutes. Add paneer cubes and cream. Simmer for 5 minutes and then serve hot with naan or rice.",
    "Pani Puri":"For the pani, blend mint leaves, coriander leaves, green chilies, tamarind pulp, and chaat masala into a smooth green chutney. Add cold water, black salt, roasted cumin powder, and black pepper. Mix well. For the puris, mix semolina, all-purpose flour, baking soda, and salt. Knead into a stiff dough and let it rest for 30 minutes. Roll the dough into small balls and flatten them. Deep fry the puris until they puff up and turn golden. For the filling, mix boiled and mashed potatoes, black chickpeas, chopped onions, and spices like chaat masala, roasted cumin powder, and black salt. Make a small hole in each puri and stuff it with the filling. Dip the filled puri into the pani and serve immediately.",
    "Rajma Chawal":"oak kidney beans overnight in water. Drain and pressure cook with water, salt, and turmeric for 15 minutes or until soft. In a pan, heat oil and add cumin seeds, bay leaf, and cinnamon stick. Add chopped onions and cook until golden. Add ginger-garlic paste and cook for a minute. Add chopped tomatoes and cook until soft. Add red chili powder, coriander powder, cumin powder, and garam masala. Cook until the oil separates. Add the cooked kidney beans along with some water and simmer for 20-30 minutes on low heat. Serve hot with steamed rice.",
    "Gulab Jamun":"For the gulab jamuns, mix khoya, all-purpose flour, baking powder, and a little ghee. Knead into a smooth dough, adding milk as needed. Make small balls from the dough. In a separate pan, heat sugar and water to make a sugar syrup. Add cardamom powder and rose water. Heat the syrup until it becomes slightly sticky. Deep fry the gulab jamuns in ghee until golden brown. Soak them in the sugar syrup for a few hours. Serve hot or cold.",
    "Vada Pav":"For the vada, mix boiled and mashed potatoes with green chilies, ginger, garlic, mustard seeds, turmeric, and salt. Shape the mixture into small balls and flatten them. Make a batter using gram flour, turmeric, red chili powder, and water. Dip the potato balls into the batter and deep fry until golden brown. For the pav, slit dinner rolls and spread some garlic chutney inside. Stuff the vada inside the pav and serve hot.",
    "Pav Bhaji":"Boil and mash vegetables like potatoes, cauliflower, peas, carrots, and beans. In a pan, heat butter and add chopped onions. Cook until golden. Add ginger-garlic paste and cook for a minute. Add chopped tomatoes and cook until soft. Add turmeric, red chili powder, pav bhaji masala, and salt. Cook until the tomatoes break down. Add the mashed vegetables and some water. Mash the vegetables and mix everything together. Serve hot with buttered pav and chopped onions.",
    "Chana Masala":"Soak chickpeas overnight in water. Drain and pressure cook with water, salt, and tea bags for 15 minutes or until soft. Discard the tea bags and keep the chickpeas aside. In a pan, heat oil and add cumin seeds and bay leaf. Add chopped onions and cook until golden. Add ginger-garlic paste and cook for a minute. Add chopped tomatoes and cook until soft. Add red chili powder, coriander powder, cumin powder, garam masala, and amchur powder. Cook until the oil separates. Add the cooked chickpeas and some water. Simmer for 10 minutes and then mash some of the chickpeas to thicken the gravy. Garnish with coriander leaves and serve hot with naan or rice.",
    "Masala Dosa":"For the dosa batter, soak rice and urad dal separately in water for 4-6 hours. Grind them together into a smooth batter, adding water as needed. Ferment the batter overnight. For the masala, heat oil and add mustard seeds, cumin seeds, and chana dal. Add chopped onions and cook until golden. Add ginger-garlic paste and cook for a minute. Add chopped tomatoes and cook until soft. Add turmeric, red chili powder, and salt. Cook until the tomatoes break down. Add boiled and mashed potatoes and mix well. For the dosa, heat a non-stick pan and spread a ladleful of batter in a circular motion. Drizzle some oil and cook until the dosa turns golden brown. Place a portion of the masala in the center of the dosa and fold it. Serve hot with coconut chutney and sambar.",
    "Tandoori Chicken":"Marinate chicken with yogurt, ginger-garlic paste, red chili powder, turmeric, garam masala, and salt. Add lemon juice and mustard oil for flavor. Let it marinate for a few hours or overnight. Preheat the oven to the highest temperature. Skewer the marinated chicken pieces and place them on a baking tray. Cook in the oven until the chicken is charred and cooked through. Serve hot with mint chutney and onion rings.",
    "Chicken Curry":"Marinate chicken with yogurt, ginger-garlic paste, red chili powder, turmeric, garam masala, and salt. Heat oil in a pan and add whole spices like bay leaves, cinnamon, cardamom, and cloves. Add chopped onions and cook until golden. Add ginger-garlic paste and cook for a minute. Add chopped tomatoes and cook until soft. Add coriander powder and cumin powder. Cook until the tomatoes break down and the oil separates. Add the marinated chicken and cook until it changes color. Add water and simmer until the chicken is cooked through and the gravy thickens. Garnish with coriander leaves and serve hot with naan or rice.",
    "Fish Curry":"Marinate fish with turmeric, red chili powder, and salt. Heat oil in a pan and add mustard seeds, fenugreek seeds, and curry leaves. Add chopped onions and cook until golden. Add ginger-garlic paste and cook for a minute. Add chopped tomatoes and cook until soft. Add coriander powder, cumin powder, turmeric, red chili powder, and tamarind pulp. Cook until the oil separates. Add water and bring to a boil. Add the marinated fish and cook until it is done. Garnish with coriander leaves and serve hot with rice.",
    "Bhindi Masala":"Heat oil in a pan and add cumin seeds. Add chopped onions and cook until golden. Add ginger-garlic paste and cook for a minute. Add chopped tomatoes and cook until soft. Add turmeric, red chili powder, coriander powder, cumin powder, and amchur powder. Cook until the tomatoes break down and the oil separates. Add chopped okra and mix well. Cook on low heat until the okra is tender and cooked through. Garnish with coriander leaves and serve hot with roti or rice.",
    "Mutton Curry":"Marinate mutton with yogurt, ginger-garlic paste, red chili powder, turmeric, garam masala, and salt. Heat oil in a pressure cooker and add whole spices like bay leaves, cinnamon, cardamom, and cloves. Add chopped onions and cook until golden. Add ginger-garlic paste and cook for a minute. Add chopped tomatoes and cook until soft. Add coriander powder and cumin powder. Cook until the tomatoes break down and the oil separates. Add the marinated mutton and cook until it changes color. Add water and pressure cook until the mutton is tender. Garnish with coriander leaves and serve hot with naan or rice.",
    "Kadai Paneer":"In a pan, dry roast coriander seeds, cumin seeds, and dried red chilies. Grind them into a coarse powder. Heat oil in a kadai and add chopped onions and capsicum. Cook until they are slightly charred. Add ginger-garlic paste and cook for a minute. Add chopped tomatoes and cook until soft. Add the ground spice mix and cook for a few minutes. Add paneer cubes and mix well. Cook for a few more minutes until the paneer is coated with the masala. Garnish with coriander leaves and serve hot with naan or rice.",
    "Dahi Puri":"For the puris, mix semolina, all-purpose flour, baking soda, and salt. Knead into a stiff dough and let it rest for 30 minutes. Roll the dough into small balls and flatten them. Deep fry the puris until they puff up and turn golden. For the filling, mix boiled and mashed potatoes, black chickpeas, chopped onions, and spices like chaat masala, roasted cumin powder, and black salt. Make a small hole in each puri and stuff it with the filling. Top with sweetened yogurt, tamarind chutney, mint chutney, and sev. Serve immediately.",
    "Hyderabadi Biryani":"Marinate chicken with yogurt, ginger-garlic paste, red chili powder, turmeric, garam masala, and salt. In a large pot, heat ghee and add whole spices like bay leaves, cinnamon, cardamom, and cloves. Add sliced onions and cook until golden. Add chopped tomatoes and cook until soft. Add coriander powder and cumin powder. Cook until the tomatoes break down and the oil separates. Add the marinated chicken and cook until it changes color. In a separate pot, parboil basmati rice with whole spices like bay leaves, cinnamon, and cardamom. Layer the partially cooked rice over the chicken and add saffron milk, fried onions, and ghee. Seal the pot tightly with dough and cook on low heat until the rice is fully cooked and the flavors meld together. Serve hot with raita.",
    "Dum Aloo":"Boil baby potatoes until they are fork-tender. In a pan, heat oil and add cumin seeds. Add chopped onions and cook until golden. Add ginger-garlic paste and cook for a minute. Add chopped tomatoes and cook until soft. Add turmeric, red chili powder, coriander powder, cumin powder, and garam masala. Cook until the tomatoes break down and the oil separates. Add the boiled potatoes and mix well. Add water and simmer until the potatoes are coated with the masala and the gravy thickens. Garnish with coriander leaves and serve hot with naan or rice.",
    "Kheer":"In a pan, bring milk to a boil. Add rice and cook on low heat until the rice is soft and the milk thickens. Add sugar, saffron, and cardamom powder. Cook for a few more minutes until the sugar dissolves. Add chopped nuts and dried fruits. Stir well and remove from heat. Serve hot or cold, garnished with more nuts and dried fruits.",
    "Phirni":"In a pan, bring milk to a boil. Add ground rice and cook on low heat until the rice is cooked and the milk thickens. Add sugar, saffron, and cardamom powder. Cook for a few more minutes until the sugar dissolves. Pour the phirni into small earthenware pots and let it cool. Refrigerate until set. Garnish with chopped nuts and serve chilled.",
    "Jalebi":"Mix all-purpose flour, cornflour, and baking soda. Add yogurt and water to make a smooth batter. Let the batter ferment for a few hours. In a separate pan, heat sugar and water to make a sugar syrup. Add cardamom powder and saffron. Heat the syrup until it becomes slightly sticky. Pour the batter into a squeeze bottle or a piping bag with a fine nozzle. Heat oil in a pan and squeeze the batter in a spiral shape. Deep fry the jalebis until they are golden and crispy. Soak them in the sugar syrup for a few minutes. Serve hot or cold.",
    "Aloo Paratha":"For the paratha dough, mix whole wheat flour, water, and salt. Knead into a soft dough. For the filling, mix boiled and mashed potatoes with chopped green chilies, ginger, cumin seeds, and spices like coriander powder and amchur powder. Divide the dough into small balls and roll them into circles. Place a portion of the filling in the center of the circle and fold the edges to seal it. Roll the stuffed dough into a flatbread. Cook the paratha on a hot griddle with ghee until golden brown and cooked through. Serve hot with yogurt, pickles, and butter.",
    "Gajar Ka Halwa":"Grate carrots and cook them in milk until soft and the milk thickens. Add sugar, ghee, and chopped nuts. Cook until the halwa is thick and the ghee separates. Garnish with more nuts and serve hot or cold.",
    "Kulfi":"In a heavy-bottomed pan, bring milk to a boil and let it simmer until it reduces to half its volume. Add sugar, cardamom powder, and saffron. Cook until the milk thickens further. Add chopped nuts and dried fruits. Pour the mixture into kulfi molds and freeze until set. Serve chilled, garnished with more nuts.",
    "Chole Tikka Chaat":"For the chole, soak chickpeas overnight in water. Drain and pressure cook with water, salt, and tea bags for 15 minutes or until soft. Discard the tea bags and keep the chickpeas aside. In a pan, heat oil and add cumin seeds and bay leaf. Add chopped onions and cook until golden. Add ginger-garlic paste and cook for a minute. Add chopped tomatoes and cook until soft. Add turmeric, red chili powder, coriander powder, cumin powder, garam masala, and amchur powder. Cook until the oil separates. Add the cooked chickpeas and some water. Simmer for 10 minutes and then mash some of the chickpeas to thicken the gravy. For the tikka, marinate paneer and vegetables with yogurt, ginger-garlic paste, red chili powder, turmeric, garam masala, and salt. Thread the paneer and vegetable pieces onto skewers and grill or bake until charred and cooked through. For the chaat, mix the chole with chopped onions, tomatoes, green chilies, coriander leaves, and lemon juice. Top with the tikka pieces and drizzle with mint chutney and tamarind chutney. Serve immediately.",
    "Pakora":"For the pakora batter, mix gram flour, rice flour, baking soda, and spices like turmeric, red chili powder, and garam masala. Add water and mix until you get a thick batter. Add chopped onions, potatoes, and spinach to the batter. Heat oil in a pan and drop spoonfuls of the batter into the hot oil. Fry until the pakoras are golden and crispy. Serve hot with mint chutney and tamarind chutney.",
    "Chicken Cafreal":"Marinate chicken with green chili paste, ginger-garlic paste, turmeric, garam masala, and vinegar. In a pan, heat oil and add chopped onions. Cook until golden. Add ginger-garlic paste and cook for a minute. Add chopped tomatoes and cook until soft. Add coriander powder, cumin powder, and red chili powder. Cook until the tomatoes break down and the oil separates. Add the marinated chicken and cook until it changes color. Add water and simmer until the chicken is cooked through and the gravy thickens. Garnish with coriander leaves and serve hot with rice or bread.",
    "Kansar":"Mix wheat flour, ghee, and jaggery. Knead into a smooth dough, adding water as needed. Shape the dough into small balls and press them with your fingers to make impressions. Steam the kansar balls until cooked. Serve hot with ghee.",
    "Modak":"For the modak filling, mix grated coconut, jaggery, and chopped nuts. Cook the mixture until the jaggery melts and the coconut mixture thickens. For the modak dough, mix rice flour with water and ghee. Knead into a smooth dough. Take a small portion of the dough and shape it into a cup. Fill the cup with the coconut filling and close the top to make a modak shape. Steam the modaks until cooked. Serve hot or cold.",
    "Gulab Jamun":"In a large bowl, mix milk powder, all-purpose flour, baking powder, and a pinch of cardamom powder. Add ghee or melted butter and mix to form a crumbly texture. Gradually add milk and knead the mixture into a soft dough. Let the dough rest for 15-20 minutes. In the meantime, prepare the sugar syrup by dissolving sugar in water and adding a few drops of rose essence. Boil the syrup until it reaches a sticky consistency. Heat oil or ghee in a pan for deep frying. Make small balls from the dough and ensure there are no cracks on the surface. Fry the gulab jamun balls on low heat until they turn golden brown and evenly cooked. Drain the excess oil and immediately transfer them to the hot sugar syrup. Let the gulab jamuns soak in the syrup for at least an hour before serving. Serve them warm, and they will be soft, sweet, and utterly delightful.",
    "Ras Malai":"For the ras malai discs, mix paneer, all-purpose flour, and baking powder. Knead into a smooth dough. Divide the dough into small balls and flatten them into discs. In a pan, bring milk to a boil. Add sugar, cardamom powder, and saffron. Let the milk simmer until it thickens. Add the paneer discs to the milk and let them cook for a few minutes. Garnish with chopped nuts and serve chilled.",
    "Veg Biryani":"Marinate mixed vegetables with yogurt, ginger-garlic paste, red chili powder, turmeric, garam masala, and salt. In a large pot, heat ghee and add whole spices like bay leaves, cinnamon, cardamom, and cloves. Add sliced onions and cook until golden. Add chopped tomatoes and cook until soft. Add coriander powder and cumin powder. Cook until the tomatoes break down and the oil separates. Add the marinated vegetables and mix well. In a separate pot, parboil basmati rice with whole spices like bay leaves, cinnamon, and cardamom. Layer the partially cooked rice over the vegetables and add saffron milk, fried onions, and ghee. Seal the pot tightly with dough and cook on low heat until the rice is fully cooked and the flavors meld together. Serve hot with raita.",
    "Shahi Paneer":"In a pan, heat ghee and add whole spices like bay leaves, cinnamon, cardamom, and cloves. Add chopped onions and cook until golden. Add ginger-garlic paste and cook for a minute. Add chopped tomatoes and cook until soft. Add cashew nuts and cook for a few minutes. Blend the mixture into a smooth paste. In the same pan, heat ghee and add cumin seeds. Add the tomato-cashew paste and cook for a few minutes. Add coriander powder, cumin powder, red chili powder, and garam masala. Cook until the masala is cooked and the oil separates. Add paneer cubes and mix well. Add water and simmer until the paneer is coated with the masala and the gravy thickens. Add cream and cook for a few more minutes. Garnish with chopped nuts and serve hot with naan or rice.",
    "Kadhi Pakora":"For the pakoras, mix gram flour, rice flour, baking soda, and spices like turmeric, red chili powder, and garam masala. Add water and mix until you get a thick batter. Add chopped onions and spinach to the batter. Heat oil in a pan and drop spoonfuls of the batter into the hot oil. Fry until the pakoras are golden and crispy. For the kadhi, mix yogurt, gram flour, turmeric, and salt. Whisk until smooth. In a pan, heat ghee and add cumin seeds, fenugreek seeds, and asafoetida. Add chopped onions and cook until golden. Add ginger-garlic paste and cook for a minute. Add chopped tomatoes and cook until soft. Add the yogurt mixture and water. Cook on low heat until the kadhi thickens. Add the pakoras and cook for a few more minutes. Garnish with coriander leaves and serve hot with rice.",
    "Rasgulla":"In a pan, bring water and sugar to a boil. Add cardamom pods for flavor. In a separate pan, bring milk to a boil. Add lemon juice or vinegar to curdle the milk. Strain the milk solids and wash them under cold water to remove the lemon juice or vinegar taste. Knead the milk solids into a smooth dough. Shape the dough into small balls and flatten them slightly. Drop the balls into the boiling sugar syrup. Cover the pan and cook on medium heat for 10-15 minutes. The rasgullas will double in size and become spongy. Let them cool in the syrup and serve chilled.",
    "Bebinca":"In a blender, mix coconut milk, egg yolks, sugar, and flour to form a smooth batter. In a baking dish, layer the batter and bake until the top is golden and the bebinca is cooked through. Serve hot or cold.",
    "Kofta Curry":"For the koftas, mix grated paneer, mashed potatoes, chopped nuts, and spices like coriander powder, cumin powder, and garam masala. Shape the mixture into small balls and deep fry until golden. For the curry, heat ghee in a pan and add whole spices like bay leaves, cinnamon, cardamom, and cloves. Add chopped onions and cook until golden. Add ginger-garlic paste and cook for a minute. Add chopped tomatoes and cook until soft. Add turmeric, red chili powder, coriander powder, cumin powder, and garam masala. Cook until the tomatoes break down and the oil separates. Add water and simmer until the gravy thickens. Add the fried koftas and cook for a few more minutes. Garnish with coriander leaves and serve hot with naan or rice.",
    "Rogan Josh":"Marinate mutton with yogurt, ginger-garlic paste, red chili powder, turmeric, garam masala, and salt. In a pan, heat ghee and add whole spices like bay leaves, cinnamon, cardamom, and cloves. Add sliced onions and cook until golden. Add chopped tomatoes and cook until soft. Add coriander powder and cumin powder. Cook until the tomatoes break down and the oil separates. Add the marinated mutton and cook until it changes color. Add water and pressure cook until the mutton is tender. Garnish with coriander leaves and serve hot with naan or rice.",
    "Shrikhand":"Hang yogurt in a muslin cloth for a few hours to remove excess water. In a bowl, mix the hung yogurt with sugar, cardamom powder, and saffron. Refrigerate until chilled. Garnish with chopped nuts and serve cold.",
    "Aloo Tikki":"Boil and mash potatoes. Add chopped green chilies, ginger, coriander leaves, and spices like coriander powder and garam masala. Mix well and shape the mixture into small flat discs. Heat oil in a pan and shallow fry the tikkis until golden and crispy. Serve hot with mint chutney and tamarind chutney.",
    "Chaat":"For the chaat, mix boiled and cubed potatoes, boiled chickpeas, chopped onions, tomatoes, and green chilies. Add spices like chaat masala, roasted cumin powder, and black salt. Top with mint chutney, tamarind chutney, and sev. Serve immediately."
}

# Preprocess the text by converting to lowercase and removing punctuation
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# Compute cosine similarity between two vectors
def cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    if norm1 == 0 or norm2 == 0:
        return 0.0  # Handle zero-length vectors
    similarity = dot_product / (norm1 * norm2)
    return similarity

# Calculate TF-IDF scores for a given recipe
def calculate_tfidf(recipe, vocabulary, document_frequencies):
    tfidf_vector = np.zeros(len(vocabulary))
    ingredients = preprocess_text(recipe).split(', ')
    for ingredient in ingredients:
        if ingredient in vocabulary:
            # Calculate term frequency (TF)
            term_frequency = ingredients.count(ingredient) / len(ingredients)

            # Calculate inverse document frequency (IDF)
            inverse_document_frequency = np.log(len(recipes) / (document_frequencies[vocabulary.index(ingredient)] + 1))

            # Calculate TF-IDF score
            tfidf_vector[vocabulary.index(ingredient)] = term_frequency * inverse_document_frequency

    return tfidf_vector


# Build a vocabulary of unique ingredients from all recipes
def build_vocabulary_and_document_frequencies(recipes):
    vocabulary = set()
    for recipe in recipes:
        ingredients = preprocess_text(recipe).split(', ')
        vocabulary.update(ingredients)

    # Initialize document frequencies with zeros for each ingredient in the vocabulary
    document_frequencies = np.zeros(len(vocabulary))

    # Count the occurrences of each ingredient in all recipes
    for recipe in recipes:
        ingredients = preprocess_text(recipe).split(', ')
        for ingredient in set(ingredients):
            document_frequencies[list(vocabulary).index(ingredient)] += 1

    return list(vocabulary), document_frequencies

# Build the vocabulary and document frequencies from all recipes
def get_recommendations(input_ingredients, recipes, recipe_names):
    vocabulary, document_frequencies = build_vocabulary_and_document_frequencies(recipes)

    # Calculate TF-IDF vector for input ingredients
    input_vector = calculate_tfidf(input_ingredients, vocabulary, document_frequencies)

    # Compute cosine similarity between input and all recipes
    similarity_scores = defaultdict(float)
    for i, recipe in enumerate(recipes):
        recipe_vector = calculate_tfidf(recipe, vocabulary, document_frequencies)
        similarity = cosine_similarity(input_vector, recipe_vector)
        similarity_scores[i] = similarity

    # Get indices of top-k most similar recipes
    k = 3  # Number of recommendations to provide
    indices = sorted(similarity_scores, key=similarity_scores.get, reverse=True)[:k]

    # Get recommended recipe names
    recommended_recipe_names = [recipe_names[i] for i in indices]

    return recommended_recipe_names,indices

# Test the recommendation system
input_ingredients = "savory snack, chutneys"
recommendations,indices = get_recommendations(input_ingredients, recipes, recipe_names)
print(indices)
print("Recommended Recipes:")
for recipe in recommendations:
    print(recipe)
    


# Streamlit app
def main():
    st.title(":orange[__Cooking Genie__]")

    # Input ingredients
    input_ingredients = st.text_input(":red[__Enter your ingredients separated by commas__]")

    if input_ingredients:
        recommendations, indices = get_recommendations(input_ingredients, recipes, recipe_names)
        st.write(":red[Which one do you want to make?]")
        for recipe_name in recommendations:
            if st.button(f"Show Instruction to build :orange[{recipe_name}]"):
                st.markdown(f"<p style='color: blue;'><b>{description[recipe_name]}</b></p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    