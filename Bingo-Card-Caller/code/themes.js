class Theme {
    constructor(id, displayName){
        this.id = id;
        this.displayName = displayName;
        this.colors = new Map(); // element mapped to colors
    }
}

var defaultTheme = new Theme("theme-default", "Default Theme");
defaultTheme.colors.set("body-background","rgb(74, 74, 74)");
defaultTheme.colors.set("toolbar", "#0074d9");
defaultTheme.colors.set("odd-number-panel", "rgb(74, 74, 74)");
defaultTheme.colors.set("even-number-panel", "#B7B600");

var halloweenTheme = new Theme("theme-halloween", "Halloween");
halloweenTheme.colors.set("body-background", "black");
halloweenTheme.colors.set("toolbar", "orange");
halloweenTheme.colors.set("odd-number-panel", "black");
halloweenTheme.colors.set("even-number-panel", "#5d4314");

var christmasTheme = new Theme("theme-christmas", "Christmas");
christmasTheme.colors.set("body-background", "rgb(0, 146, 9)");
christmasTheme.colors.set("toolbar", "rgb(217, 0, 0)");
christmasTheme.colors.set("odd-number-panel", "rgb(28, 79, 0)");
christmasTheme.colors.set("even-number-panel", "rgb(0, 146, 9)");

var themes = new Map();
themes.set(defaultTheme.id, defaultTheme);
themes.set(halloweenTheme.id, halloweenTheme);
themes.set(christmasTheme.id, christmasTheme);