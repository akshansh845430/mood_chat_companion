import random

RESPONSES = {
    "angry": [
        "Oof… that spark in your voice? Pure lava. Bolo, kiski bajaani hai aaj? But seriously — breathe. Tell me who poked the volcano.",
        "Gussa… itna ki microphone bhi dar gaya. Chal, saari baat ugal do. I won’t judge — I’ll just hold the fire with you.",
        "Your tone is sharp… like a sword that’s tired of being silent. What pushed you this far? Let it out — main yahin hoon.",
        "Awaaz mein woh kadwaahat hai… jaise chai mein cheeni bhool gaye ho. Come on, drop the truth — kya chal raha hai?",
        "That frustration you’re carrying feels heavy… like you’ve been fighting storms alone. Throw the thunder here — I can take it."
    ],

    "happy": [
        "Arre wah! Aaj toh tumhari awaaz mein full Diwali lighting jhalak rahi hai. Batao, kya khush khabri mili?",
        "Your voice is literally smiling. Matlab agar voice ko selfie mode hota, it would be glowing right now.",
        "There’s a sparkle in your tone — mujhe lagta hai kuch accha hua hai. Spill the good news!",
        "Aaj toh lagta hai duniya tumhare flavor mein bani hai. Come, share the recipe of this happiness.",
        "You sound like a weekend morning — soft, sunny, and full of good vibes. Tell me, what stirred this joy?"
    ],

    "neutral": [
        "Hmm… tumhari awaaz bilkul chai ke pehle sip jaisi lag rahi hai — calm, warm, steady. What’s brewing inside?",
        "Neutral huh… jaise life ne pause button dabaa diya ho. Koi baat nahi — I’m here. Kabhi kabhi silence bhi story hoti hai.",
        "Your tone feels like a long walk on an empty road… peaceful, maybe thoughtful. What’s wandering in that mind of yours?",
        "I sense calmness… par kabhi kabhi calm ke peeche dhoop bhi hoti hai, kabhi dard bhi. Tell me, where’s your heart leaning today?",
        "Awaaz bilkul sant, bilkul thandi. But I know… even still water has stories at the bottom. Want to share one?"
    ],

    "sad": [
        "Your voice feels like a poem left unfinished… soft, heavy, waiting. Batao, kya bojh hai dil par?",
        "Hmm… I can hear that drop in your tone. Jaise baarish aane wali ho… and I don’t want you to stand in it alone. Talk to me.",
        "There’s a quiet pain in your voice… the kind that hides behind long pauses. Mujhe batao, what’s hurting?",
        "Dil halka kar lo yahan… main kahin nahi jaa raha. Your voice feels like you’ve been carrying too much for too long.",
        "Aaj tumhari awaaz thodi halki si tooti hui lag rahi hai… jaise koi baat andar dabakar rakhi ho. Let it out — I’m listening, truly."
    ]
}

def get_response(emotion):
    if emotion not in RESPONSES:
        return "Mood thoda confusing lag raha hai… but no worries, I’m right here. Tell me anything."

    return random.choice(RESPONSES[emotion])
