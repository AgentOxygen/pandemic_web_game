# Pandemic Game
Based on the board game Pandemic

## JavaScript Layout


## Flask Routes


## Redis
*Key format:* '[Game Instance ID]-[Directory]-[Tag]'
*List of keys for every game instance:*

'[Game Instance ID]-[Info]'
> JSON containing current game info including the number of outbreaks, infection rate, disease counts, played and unplayed player cards, played and unplayed infection cards

'[Game Instance ID]-[Cures]'
> JSON containing status of cures

'[Game Instance ID]-[Players]'
> JSON containing list of active players and their respective IDs

'[Game Instance ID]-[Players]-[Player ID]'
> JSON containing role of player and cards withheld

'[Game Instance ID]-[Cities]'
> JSON containing cities and their respective disease counts



## Assets

US Map - https://pixabay.com/vectors/usa-map-united-states-of-america-35713/
Diseases - https://dribbble.com/shots/11020766-Free-Coronavirus-Vector-Ai-EPS-Color-Schemes
Medic - https://graphicsurf.com/item/medical-vector-free-icon-set/
Scientist - https://graphicsurf.com/item/medical-vector-free-icon-set/
Quarantine Specialist - https://graphicsurf.com/item/medical-vector-free-icon-set/
Logistics Operator - https://graphicsurf.com/item/medical-vector-free-icon-set/
Researcher - https://graphicsurf.com/item/medical-vector-free-icon-set/