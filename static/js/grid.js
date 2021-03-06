(function (root, module) {

    root.Grid = module();

})(window, function () {


    Grid.prototype.re_index_forms = function () {
        // this fixes a bug
        // hithero i'd assumed, for example, we post two forms,
        // form_1 and form_4 as part of a django formset
        // except we cannot.
        // django will see the form count is 2 and so construct a form_1
        // and a form_2.  Each then is passed POST data where the prefix index
        // is the same as the form index.
        // this means clientside we must ensure our forms are consecutively indexed
        this.get_table()
            .find("tbody")
            .find("tr")
            .not(this.empty_form_identifier)
            .each(function (row_index, row) {
                var $row = $(row);
                $row.find(":input").each(function(i, field){
                    field = $(field);
                    var name = $(field).attr("name");
                    if(name){
                        name = name.replace(/\d+/, row_index);
                        field.attr("name", name);
                    }
                });
            });
    };


    Grid.prototype.delete_line = function (delete_button) {
        // assume delete button is in the line to delete
        // pretty dumb otherwise
        delete_button.parents("tr").eq(0).remove();
        this.set_total_forms(this.get_total_forms() - 1);
        this.reorder();
    };

    Grid.prototype.get_order = function (row_index, $row) {
        var order;
        $row.find(":input:visible").each(function (field_index, field) {
            var field = $(field);
            if (field.attr("type") == "checkbox") {
                if (field.prop("checked")) {
                    order = row_index;
                    return false; // end the loop
                }
            }
            else {
                if (field.val()) {
                    order = row_index;
                    return false; // end the loop
                }
            }
        });
        return order;
    };

    Grid.prototype.reorder = function () {
        if (!this.order_lines) {
            console.log("WARNING: you have ordering diabled!");
        }
        var instance = this;
        this.get_table()
            .find("tbody")
            .find("tr")
            .not(this.empty_form_identifier)
            .each(function (row_index, row) {
                var $row = $(row);
                var order = instance.get_order(row_index, $row);
                if (order != undefined) {
                    // only order the row if any of the visible fields are not blank
                    // otherwise visibly empty forms will be validated on the server because on the server side
                    // the order input field has a value set
                    $row.find("input" + instance.order_identifier).val(order);
                }
            });
        this.re_index_forms();
    };


    Grid.prototype.add_many_lines = function (n) {
        for (var i = 0; i < n; i++) {
            this.add_line();
        }
    };


    Grid.prototype.add_line = function () {
        var next_line = this.get_empty_form().clone();
        var total_forms = this.get_total_forms();
        next_line = next_line.wrap("<p/>").parent().html();
        next_line = next_line.replace(/__prefix__/g, total_forms);
        next_line = $(next_line);
        next_line.removeClass("d-none").removeClass("empty-form");
        next_line.find("input").each(function () {
            $(this).val("");
        });
        this.get_table().find("tbody").append(next_line);
        this.set_total_forms(total_forms + 1);
        this.reorder();
        if (this.add_callback) {
            this.add_callback(next_line);
        }
    };

    // calling code example
    // var grid = Grid(opts);
    // $(".add_invoice_button").on("click", function(event){
    //     grid.add_line();
    //     event.stopPropagation();
    // });


    Grid.prototype.set_total_forms = function (count) {
        $(this.form_identifier).find("input[name='" + this.prefix + "-TOTAL_FORMS']").val(count);
    };


    Grid.prototype.get_total_forms = function () {
        return +$(this.form_identifier).find("input[name='" + this.prefix + "-TOTAL_FORMS']").val();
    };


    Grid.prototype.get_table = function () {
        return $(this.table);
    };

    Grid.prototype.get_empty_form = function () {
        return $(this.table).find("tr" + this.empty_form_identifier);
    };


    function enable_jquery_sorting(grid) {
        grid.get_table().find("tbody").sortable({
            placeholder: "ui-state-highlight",
            handle: ".col-draggable-icon",
            update: function (event, ui) {
                grid.reorder();
            },
            helper: function (e, ui) {
                // without this helper the table width is the sum of
                // the content width per each column
                // Setting the width per row does not work so must
                // be done for each th and td element instead
                ui.parents("table").find("th, td").each(function () {
                    $(this).width($(this).width());
                });
                return ui;
            }
        });
        grid.get_table().find("tbody").disableSelection();
    }


    // Example options
    // {
    //     prefix: "line", // form prefix
    //     form_identifier: "lines", // wrapper for grid
    //     order_lines: true, // is ordering enabled
    //     order_identifier: ".ordering"
    //     empty_form_identifier: ".empty_form",
    //     add_callback: function called when a line has been added
    //                   is passed the new line
    // }


    function Grid(opts) {
        this.prefix = opts.form_prefix || "line";
        this.form_identifier = opts.form_identifier || "line";
        this.empty_form_identifier = opts.empty_form_identifier || ".empty-form";
        // we expect the grid table to have the prefix
        this.table = "table." + this.prefix;
        this.order_lines = opts.order_lines || true;
        this.order_identifier = opts.order_identifier || ".ordering";
        if (this.order_lines) {
            enable_jquery_sorting(this);
        }
    }


    return Grid;

});