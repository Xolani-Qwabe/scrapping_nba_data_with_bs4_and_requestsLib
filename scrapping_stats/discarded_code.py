#returns away_team, home_team, date
# def extract_info_from_string(game_string):
#     parts = split_game_details_to_list(game_string)
#     print(parts)
#     away_team = f'{parts[0]} {parts[1]}'
#     home_team = f'{parts[2]} {parts[3]}'
#     date_info = parts[4]
#     date_obj = datetime.strptime(date_info, '%B%d%Y')
#     formatted_date = date_obj.strftime('%Y-%m-%d')
#     return away_team, home_team, formatted_date

# def split_game_details_to_list(game_string):
#     print(game_string)
#     part_list = game_string.split('_', 1)
#     my_list = r.findall(r'([A-Z][a-z0-9]*)', part_list[0])
#     my_list.append(part_list[1])
#     print(my_list)
#     if len(my_list) == 8 and my_list[1].endswith('at'):
#         print('2nd item ends with @')
#         item = my_list[1][:-2]
#         my_list.insert(1, item)
#         my_list.remove("Box")
#         if "Score" in my_list:
#             my_list.remove("Score")
#         else:
#             my_list.remove("Score_")
#         joined_team_name = ' '.join(my_list[3:5])
#         new_list = (my_list[0:2]+my_list[-3:])
#         new_list.insert(2,joined_team_name)
#         (new_list.pop(3))
#         return list(map(lambda i: i.replace("_", ""), new_list))
#     elif len(my_list) == 8 and my_list[2].endswith('at'):
#         print('3rd item ends with @')
#         item = my_list[2][:-2]
#         my_list.insert(2, item)
#         my_list.pop(3)
#         my_list.remove("Box")
#         if "Score" in my_list:
#             my_list.remove("Score")
#         else:
#             my_list.remove("Score_")
#         joined_team_name = ' '.join(my_list[0:2])
#         new_list = (my_list[2:])
#         new_list.insert(0, joined_team_name)
#         return list(map(lambda i: i.replace("_", ""), new_list))
#     if len(my_list) == 9 and my_list[2].endswith('at'):
#         print('3rd item ends with @ and has 9 items')
#         item = my_list[2][:-2]
#         my_list.pop(2)
#         my_list.insert(2,item)
#         team1 = ' '.join(my_list[0:2])
#         team2 = ' '.join(my_list[3:5])
#         new_list = (my_list[2:3]+my_list[5:])
#         new_list.remove("Box")
#         if "Score" in new_list:
#             new_list.remove("Score")
#         else:new_list.remove("Score_")
#         new_list.insert(0,team1)
#         new_list.insert(2,team2)
#         return list(map(lambda i: i.replace("_", ""), new_list))
#     else:
#         item = my_list[1][:-2]
#         my_list.insert(1, item)
#         my_list.pop(2)
#         my_list.remove("Box")
#         if "Score" in my_list:
#             my_list.remove("Score")
#         else:
#             my_list.remove("Score_")
#         return list(map(lambda i: i.replace("_", ""), my_list))

