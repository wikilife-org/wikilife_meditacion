function FoodPieChart (values) {

    this.piechartRadius = 88;
    this.margin = 50;
    this.colors = [ "#3e8087", "#63cece", "#a8fffd", "#ffff00", "#f08a00", "#e75113" ];
    
    this.amount = values.length;

    var accValues = [];
    accValues[0] = values[0];
    for (i = 1; i < this.amount; i++)
        accValues[i] = accValues[i - 1] + values[i];

    var radianValues = [];
    for (i = 0; i < this.amount; i++)
        radianValues[i] = accValues[i] * 2 * Math.PI / 100;

    var stage = new Kinetic.Stage({
        container : "pieChart",
        width : 277,
        height : 277
    });
    var layer = new Kinetic.Layer();

    layer.add(this
            ._createPortionForVariable(0, radianValues[0], this.colors[0]));
    for (i = 1; i < this.amount; i++) {
        layer.add(this._createPortionForVariable(radianValues[i - 1],
                radianValues[i], this.colors[i]));
    }

    var innerCircle = new Image();
    innerCircle.onload = function () {
        var yoda = new Kinetic.Image({
            x : 79,
            y : 79,
            image : innerCircle,
            width : 118,
            height : 118
        });
        layer.add(yoda);
        stage.draw();
    };
    innerCircle.src = '/static_media/img/circle-inner.png';

    stage.add(layer);

}

FoodPieChart.prototype._createPortionForVariable = function (accValue, value, color) {
    var that = this;

    centre = this.piechartRadius + this.margin;

    return new Kinetic.Shape({
        drawFunc : function (canvas) {
            var context = canvas.getContext();
            context.beginPath();
            // goto pieChart centre
            context.moveTo(centre, centre);
            // draw a line from the centre to the start of the arc
            context.lineTo(that._calculateXforAngle(accValue), that
                    ._calculateYforAngle(accValue));
            context.arc(centre, centre, that.piechartRadius, accValue, value);
            // goto pieChart centre
            context.moveTo(centre, centre);
            // draw a line from the centre to the end of the arc
            context.lineTo(that._calculateXforAngle(value), that
                    ._calculateYforAngle(value));
            context.closePath();
            canvas.fillStroke(this);
        },
        fill : color,
        stroke : color,
        strokeWidth : 1
    });
};

FoodPieChart.prototype._calculateXforAngle = function (angle) {
    res = this.piechartRadius * Math.cos(angle) + this.margin
            + this.piechartRadius;
    return res;
};

FoodPieChart.prototype._calculateYforAngle = function (angle) {
    return this.piechartRadius * Math.sin(angle) + this.margin
            + this.piechartRadius;
};


