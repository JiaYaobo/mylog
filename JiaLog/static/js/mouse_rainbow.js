    // 获取canvas元素
    var cvs = document.querySelector("canvas");
    // 获取上下文对象
    var ctx = cvs.getContext("2d");
    // 声明一个空数组，用来放后面生成的小球
    var ballsArr = [];

    $(function(){  //设置画布为全屏模式
        var canvas = $('#canvas');
        canvas.attr("width",$(window).get(0).innerWidth)
        canvas.attr("height",$(window).get(0).innerHeight)
        var context = canvas.get(0).getContext("2d");
        context.fillRect(0,0,canvas.width(),canvas.height());
        $(window).resize(function(){
            canvas.attr("width",$(window).get(0).innerWidth)
            canvas.attr("height",$(window).get(0).innerHeight)
            context.fillRect(0,0,canvas.width(),canvas.height());
        });
    });

    // 创建一个小球类
    function Balls (x, y){
        // 坐标x为传进来的x
        this.x = x;
        // 坐标y为传进来的y
        this.y = y;
        // 生成的小球半径为5到10中的任一整数（参数随便）
        this.r = _.random(5, 10);
        // 生成的小球的颜色为这七种颜色中的随机一种（参数随便）
        this.c = _.sample(["red", "orange", "yellow", "green", "cyan", "blue", "white"]);
        // 小球坐标x的增量为-4到4之间的整数（参数随便）
        this.dx = _.random(-4, 4);
        // 小球坐标y的增量为-4到4之间的整数（参数随便）
        this.dy = _.random(-4, 4);
        // 把生成的小球存入数组ballsArr
        ballsArr.push(this);
    }

    // 给所有Balls绑定一个方法update，目的是为了每次都能按照随机方向移动
    Balls.prototype.update = function (){
        // 每次x坐标加上增量dx
        this.x += this.dx;
        // 每次y坐标加上增量dy
        this.y += this.dy;
        // 每次半径缩小0.5（参数随便）
        this.r -= 0.5;
        // 半径小于等于0的话，就从小球数组中移出
        if(this.r <= 0){
            _.without(ballsArr, this);
        }
    }

    // 给所有Balls绑定一个方法render，目的是画圆。
    Balls.prototype.render = function (){
        // 半径小于等于0就没必要画了
        if(this.r <= 0){
            return;
        }
        // 开始绘制
        ctx.beginPath();
        // 绘制圆形，（圆心坐标x，圆心坐标y， 起始弧度，终止弧度，[顺逆时针]）
        ctx.arc(this.x, this.y, this.r, 0, 2*Math.PI);
        // 颜色为数组中随机的一个
        ctx.fillStyle = this.c;
        // 画上画布
        ctx.fill();
        // 终止绘制
        ctx.closePath();
    }

    // onmousemove事件监听
    cvs.onmousemove = function (){
        // 在当前鼠标的位置，生成俩球，然后只要鼠标移动就一直生成小球，每次两个
        new Balls(event.offsetX, event.offsetY);
        new Balls(event.offsetX, event.offsetY);
    }

    // setInterval 模拟25FPS的帧率
    setInterval(function (){
        // 因为canvas上屏即像素化，所以先清屏
        ctx.clearRect(0, 0, cvs.width, cvs.height);
        // _.each方法是针对每一个前面的元素，都运行后面的方法
        _.each(ballsArr, function (value){
            value.update();
            value.render();
        });
    }, 40);