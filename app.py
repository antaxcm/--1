import streamlit as st
import pandas as pd
import random
import json
import os
from character import Character
from data_manager import DataManager
from dnd_data import races, classes, backgrounds, ability_descriptions

# Set page configuration
st.set_page_config(
    page_title="Генератор персонажей D&D",
    page_icon="🎲",
    layout="wide"
)

# Initialize session state for storing character data
if 'character' not in st.session_state:
    st.session_state.character = Character()

if 'saved_message' not in st.session_state:
    st.session_state.saved_message = ""

if 'loaded_message' not in st.session_state:
    st.session_state.loaded_message = ""

# Create data manager instance
data_manager = DataManager()

# Main title
st.title("🎲 Генератор персонажей D&D")

# Sidebar for navigation
with st.sidebar:
    st.header("Навигация")
    page = st.radio("", ["Создать персонажа", "Загрузить персонажа"])
    
    st.header("О программе")
    st.write("Это приложение помогает создавать и управлять персонажами для Dungeons & Dragons 5-й редакции.")
    
    st.markdown("---")
    st.write("Сделано с ❤️ на Streamlit")

# Create Character Page
if page == "Создать персонажа":
    # Two-column layout for character creation
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.header("Детали персонажа")
        
        # Basic Information
        name = st.text_input("Имя персонажа", value=st.session_state.character.name)
        
        # Race Selection
        race_options = list(races.keys())
        selected_race = st.selectbox("Раса", race_options, index=race_options.index(st.session_state.character.race) if st.session_state.character.race in race_options else 0)
        
        if selected_race:
            st.write(f"**Особенности расы:** {races[selected_race]['description']}")
            
            # Русские названия характеристик
            ability_names_ru = {
                "Strength": "Сила",
                "Dexterity": "Ловкость",
                "Constitution": "Телосложение",
                "Intelligence": "Интеллект",
                "Wisdom": "Мудрость",
                "Charisma": "Харизма"
            }
            
            # Преобразуем строки с бонусами характеристик в русские названия
            bonuses_ru = [f'+{v} {ability_names_ru[k]}' for k, v in races[selected_race]['ability_bonuses'].items()]
            st.write(f"**Увеличение характеристик:** {', '.join(bonuses_ru)}")
        
        # Class Selection
        class_options = list(classes.keys())
        selected_class = st.selectbox("Класс", class_options, index=class_options.index(st.session_state.character.character_class) if st.session_state.character.character_class in class_options else 0)
        
        if selected_class:
            st.write(f"**Особенности класса:** {classes[selected_class]['description']}")
            st.write(f"**Кость хитов:** d{classes[selected_class]['hit_die']}")
            
            # Русские названия характеристик
            ability_names_ru = {
                "Strength": "Сила",
                "Dexterity": "Ловкость",
                "Constitution": "Телосложение",
                "Intelligence": "Интеллект",
                "Wisdom": "Мудрость",
                "Charisma": "Харизма"
            }
            
            # Преобразуем первичные характеристики класса на русский
            primary_abilities_ru = [ability_names_ru[ability] for ability in classes[selected_class]['primary_abilities']]
            st.write(f"**Основные характеристики:** {', '.join(primary_abilities_ru)}")
        
        # Background Selection
        background_options = list(backgrounds.keys())
        selected_background = st.selectbox("Предыстория", background_options, index=background_options.index(st.session_state.character.background) if st.session_state.character.background in background_options else 0)
        
        if selected_background:
            st.write(f"**Особенности предыстории:** {backgrounds[selected_background]['description']}")
        
        # Generate ability scores button
        if st.button("Бросить кости характеристик"):
            ability_scores = {}
            for ability in ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]:
                # Roll 4d6, remove lowest die
                rolls = [random.randint(1, 6) for _ in range(4)]
                rolls.sort(reverse=True)
                ability_scores[ability] = sum(rolls[:3])
            
            # Update character with new rolls
            st.session_state.character.ability_scores = ability_scores
            st.rerun()
    
    with col2:
        st.header("Характеристики")
        
        # Display current ability scores and modifiers
        ability_scores = st.session_state.character.ability_scores
        
        if not ability_scores:
            st.info("Нажмите 'Бросить кости характеристик' для генерации случайных значений по правилам D&D (4d6, убрать наименьшее).")
        else:
            # Русские названия характеристик
            ability_names_ru = {
                "Strength": "Сила",
                "Dexterity": "Ловкость",
                "Constitution": "Телосложение",
                "Intelligence": "Интеллект",
                "Wisdom": "Мудрость",
                "Charisma": "Харизма"
            }
            
            for ability, score in ability_scores.items():
                # Calculate racial bonus if any
                racial_bonus = races[selected_race]['ability_bonuses'].get(ability, 0)
                total_score = score + racial_bonus
                modifier = (total_score - 10) // 2
                
                # Display ability with modifier and explanation
                modifier_display = f"+{modifier}" if modifier >= 0 else f"{modifier}"
                
                st.markdown(f"**{ability_names_ru[ability]}: {total_score}** ({score} + {racial_bonus} расовый бонус) [Модификатор: {modifier_display}]")
                st.caption(ability_descriptions[ability])
        
        st.markdown("---")
        
        # Display inventory based on class
        st.subheader("Стартовое снаряжение")
        if selected_class:
            equipment = classes[selected_class]['starting_equipment']
            for item in equipment:
                st.write(f"• {item}")
    
    # Save character section
    st.markdown("---")
    if st.button("Сохранить персонажа"):
        # Update character object with current form values
        st.session_state.character.name = name
        st.session_state.character.race = selected_race
        st.session_state.character.character_class = selected_class
        st.session_state.character.background = selected_background
        
        # Save to file using data manager
        success = data_manager.save_character(st.session_state.character)
        if success:
            st.session_state.saved_message = f"Персонаж '{name}' успешно сохранен!"
            st.success(st.session_state.saved_message)
        else:
            st.error("Не удалось сохранить персонажа. Пожалуйста, попробуйте снова.")

# Load Character Page
elif page == "Загрузить персонажа":
    st.header("Загрузить персонажа")
    
    # Get all saved characters
    saved_characters = data_manager.get_saved_characters()
    
    if not saved_characters:
        st.info("Сохраненных персонажей не найдено. Сначала создайте нового персонажа!")
    else:
        # Русские названия столбцов
        column_names = {
            'name': 'Имя',
            'race': 'Раса',
            'character_class': 'Класс',
            'level': 'Уровень'
        }
        
        # Display characters in a table
        characters_df = pd.DataFrame(saved_characters)
        # Создаем копию с переименованными столбцами для отображения
        display_df = characters_df[['name', 'race', 'character_class', 'level']].copy()
        display_df.columns = [column_names[col] for col in display_df.columns]
        st.dataframe(display_df, use_container_width=True)
        
        # Select character to load
        selected_character_name = st.selectbox("Выберите персонажа для загрузки", 
                                              [char['name'] for char in saved_characters])
        
        if st.button("Загрузить выбранного персонажа"):
            # Find the selected character data
            selected_char_data = next((char for char in saved_characters if char['name'] == selected_character_name), None)
            
            if selected_char_data:
                # Load character into session state
                st.session_state.character = Character(**selected_char_data)
                st.session_state.loaded_message = f"Персонаж '{selected_character_name}' успешно загружен!"
                st.success(st.session_state.loaded_message)
                
                # Show character details
                st.subheader("Детали персонажа")
                col1, col2 = st.columns(2)
                
                # Русские названия характеристик
                ability_names_ru = {
                    "Strength": "Сила",
                    "Dexterity": "Ловкость",
                    "Constitution": "Телосложение",
                    "Intelligence": "Интеллект",
                    "Wisdom": "Мудрость",
                    "Charisma": "Харизма"
                }
                
                with col1:
                    st.write(f"**Имя:** {selected_char_data['name']}")
                    st.write(f"**Раса:** {selected_char_data['race']}")
                    st.write(f"**Класс:** {selected_char_data['character_class']}")
                    st.write(f"**Предыстория:** {selected_char_data['background']}")
                
                with col2:
                    st.write("**Характеристики:**")
                    for ability, score in selected_char_data['ability_scores'].items():
                        modifier = (score - 10) // 2
                        modifier_display = f"+{modifier}" if modifier >= 0 else f"{modifier}"
                        st.write(f"- {ability_names_ru[ability]}: {score} [{modifier_display}]")
                
                st.subheader("Стартовое снаряжение")
                if selected_char_data['character_class']:
                    equipment = classes[selected_char_data['character_class']]['starting_equipment']
                    for item in equipment:
                        st.write(f"• {item}")
            else:
                st.error("Ошибка загрузки персонажа. Пожалуйста, попробуйте снова.")
