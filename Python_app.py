
from flask import Flask, render_template_string, request

app = Flask(__name__)

# 🌟 现在每个人有：名字、密码问题、答案、留言
秘密口袋 = {
    "小明": {
        "问题": "你最喜欢的游戏是什么？",
        "答案": "我的世界",  # 正确答案
        "留言": "小明！周末一起玩我的世界吧！🎮"
    },
    "小红": {
        "问题": "我们第一次见面是在哪里？",
        "答案": "图书馆",
        "留言": "小红，那天在图书馆遇见你真开心！📚"
    },
    "小刚": {
        "问题": "我的外号是什么？",
        "答案": "大熊猫",
        "留言": "小刚，只有你会叫我大熊猫，哈哈！🐼"
    }
}

魔法网页 = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🔐 秘密留言板</title>
    <style>
        body {
            background: linear-gradient(135deg, #a8edea, #fed6e3);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Microsoft YaHei';
        }
        .卡片 {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            max-width: 450px;
            width: 90%;
            text-align: center;
        }
        h1 {
            color: #5b7b94;
            margin-bottom: 5px;
        }
        .步骤提示 {
            color: #888;
            font-size: 14px;
            margin-bottom: 25px;
        }
        .输入组 {
            margin: 15px 0;
            text-align: left;
        }
        .输入组 label {
            display: block;
            color: #555;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input {
            padding: 12px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            width: 100%;
            box-sizing: border-box;
            transition: border-color 0.3s;
        }
        input:focus {
            border-color: #5b7b94;
            outline: none;
        }
        button {
            margin-top: 20px;
            padding: 12px 40px;
            font-size: 18px;
            background: #5b7b94;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s;
        }
        button:hover {
            background: #4a6a80;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .留言盒子 {
            margin-top: 25px;
            padding: 20px;
            border-radius: 15px;
            font-size: 18px;
            line-height: 1.6;
            min-height: 40px;
        }
        .成功 {
            background: #e8f5e9;
            border: 2px solid #81c784;
            color: #2e7d32;
        }
        .失败 {
            background: #ffebee;
            border: 2px solid #ef9a9a;
            color: #c62828;
        }
        .错误 {
            background: #fff3e0;
            border: 2px solid #ffcc80;
            color: #e65100;
        }
    </style>
</head>
<body>
    <div class="卡片">
        <h1>🔐 秘密留言</h1>
        <p class="步骤提示">输入你的名字，回答秘密问题</p >
        
        <form method="POST">
            <div class="输入组">
                <label>👤 你的名字</label>
                <input type="text" name="name" placeholder="输入名字..." 
                       value="{{ name_value }}" required>
            </div>
            
            {% if question %}
            <div class="输入组">
                <label>❓ {{ question }}</label>
                <input type="text" name="answer" placeholder="你的答案..." required>
            </div>
            {% endif %}
            
            <button type="submit">
                {% if question %}
                🔓 验证并查看留言
                {% else %}
                ➡️ 下一步
                {% endif %}
            </button>
        </form>
        
        {% if message %}
        <div class="留言盒子 {{ msg_type }}">{{ message }}</div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def 首页():
    留言 = None
    问题 = None
    名字值 = ''
    消息类型 = ''
    
    if request.method == 'POST':
        名字 = request.form.get('name', '').strip()
        答案 = request.form.get('answer', '').strip()
        名字值 = 名字
        
        # 第一步：检查名字是否存在
        if 名字 not in 秘密口袋:
            if not 答案:  # 还没到回答问题的步骤
                留言 = f"❌ 没有找到「{名字}」的留言！<br>请检查名字是否正确～"
                消息类型 = '错误'
            else:
                留言 = f"❌ 「{名字}」不在名单里哦！"
                消息类型 = '错误'
        else:
            # 第二步：如果有答案，验证答案
            if 答案:
                正确答案 = 秘密口袋[名字]["答案"]
                if 答案 == 正确答案:
                    留言 = f"✅ 验证成功！<br><br>{秘密口袋[名字]['留言']}"
                    消息类型 = '成功'
                else:
                    留言 = "❌ 答案错误！再想想吧～"
                    消息类型 = '失败'
                    问题 = 秘密口袋[名字]["问题"]  # 让他重新回答
                    名字值 = 名字
            else:
                # 还没回答问题，显示问题
                问题 = 秘密口袋[名字]["问题"]
                名字值 = 名字
                留言 = None
    
    return render_template_string(魔法网页, 
                                   message=留言, 
                                   question=问题, 
                                   name_value=名字值,
                                   msg_type=消息类型)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)