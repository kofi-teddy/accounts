(function(root, module){
    root.calculator = module();
})(window, function(){

    var header_transaction_pk = "{{ main_header.pk }}";
    var header_transaction_type = "{{ header_type }}" || "{{ main_header.type }}";
    var negative_transaction_types = "\"{{ negative_transaction_types|safe }}\"";
    negative_transaction_types = JSON.parse(negative_transaction_types);

    function calculate_vat(goods, vat_rate) {
        if (goods && vat_rate) {
            var v = ((+goods * 100 * +vat_rate) / (100 * 100));
            v += 0; // avoid negative zero
            v = v.toFixed(2)
            return v;
        }
        return "";
    }

    function get_elements(tr) {
        var goods = tr.find(":input").filter(function (index) {
            return this.name.match(/line-\d+-goods/);
        });
        var vat_code = tr.find(":input").filter(function (index) {
            return this.name.match(/line-\d+-vat_code/);
        });
        var vat = tr.find(":input").filter(function (index) {
            return this.name.match(/^line-\d+-vat$/);
        });
        return {
            goods: goods,
            vat_code: vat_code,
            vat: vat,
            delete: tr.hasClass("deleted-row")
        };
    }

    function get_vat_rate($select){
        // sometimes we have a selectized select widget (create mode or user edited in edite mode)
        // other times a native widget (edit mode but not editing)
        var rate = $select.attr("data-rate");
        if(!rate){
            rate = $select.find(":selected").attr("data-rate");
        }
        return rate;
    }

    function calculate_totals() {
        // first calculate the totals for goods, vat and total
        var lines = $("table.line").find("tbody").find("tr").not("tr.empty-form, tr.deleted-row");
        var goods;
        var vat;
        var total;
        if (lines.length) {
            goods = 0;
            vat = 0;
            lines.each(function (index, line) {
                var elements = get_elements($(line));
                if (!elements.delete) {
                    var g = (+elements.goods.val() || 0) * 100;
                    var v = (+elements.vat.val() || 0) * 100;
                    goods = goods + g;
                    vat = vat + v;
                }
            });
            total = goods + vat;
            goods = goods / 100;
            vat = vat / 100;
            total = total / 100;
        } else {
            goods = 0;
            vat = 0;
            total = $("input[name='header-total']").val();
            total = +total;
        }
        // second calculate the totals for matched and due
        var existing_matches = $("table.existing_matched_transactions").find("tbody").find("tr").not("tr.empty-form");
        var new_matches = $("table.new_matched_transactions").find("tbody").find("tr").not("tr.empty-form");
        var matched_total = 0;
        existing_matches.each(function (index, tr) {
            var elem = $(tr).find(":input").filter(function (index) {
                return this.name.match(/match-\d+-value/);
            });
            var tran_type = $(tr).find(":input").filter(function (index) {
                return this.name.match(/match-\d+-type/);
            });
            var match_value = (+elem.val() || 0);
            if(negative_transaction_types.indexOf(tran_type.val()) != -1){
                match_value *= -1; // as values stored in db as negatives are shown as positives in UI
                // we need to flip sign.  Only true for negative transaction types like credit notes and payments.
            }
            var matched_by = $(tr).find(":input").filter(function (index) {
                return this.name.match(/match-\d+-matched_by/);
            });
            match_value *= -1
            match_value = (match_value * 100);
            matched_total = matched_total + match_value;
        });
        new_matches.each(function (index, tr) {
            var elem = $(tr).find(":input").filter(function (index) {
                return this.name.match(/match-\d+-value/);
            });
            var tran_type = $(tr).find(":input").filter(function (index) {
                return this.name.match(/match-\d+-type/);
            });
            var match_value = (+elem.val() || 0);
            if(negative_transaction_types.indexOf(tran_type.val()) != -1){
                match_value *= -1; // as values stored in db as negatives are shown as positives in UI
                // we need to flip sign.  Only true for negative transaction types like credit notes and payments.
            }
            match_value *= -1;
            match_value *= 100;
            matched_total = matched_total + match_value;          
        });
        if(negative_transaction_types.indexOf(header_transaction_type) != -1){
            matched_total *= -1
        }
        matched_total = matched_total / 100;
        matched_total += 0;
        var due = total - matched_total;
        goods += 0; // avoid negative zero
        goods = goods.toFixed(2);
        vat += 0;
        vat = vat.toFixed(2);
        total += 0;
        total = total.toFixed(2);
        $("td.goods-total-lines").text(goods);
        $("td.vat-total-lines").text(vat);
        $("td.total-lines").text(total);
        matched_total += 0;
        matched_total = matched_total.toFixed(2);
        due += 0;
        due = due.toFixed(2);
        var matched_total_elem = $("td.matched-total");
        var due_total_elem = $("td.due-total");
        matched_total_elem.text(matched_total);
        due_total_elem.text(due);
    }

    return {
        calculate_vat: calculate_vat,
        get_vat_rate: get_vat_rate,
        get_elements: get_elements,
        calculate_totals: calculate_totals
    };

});


$(document).ready(function () {

    $("table.line").on("change", ":input", function (event) {
        var input = $(this);
        var tr = input.parents("tr").eq(0);
        var elements = calculator.get_elements(tr);
        // calculate the VAT if the user changed value in field other than vat
        // because they may want to override
        if (
            !(
                $(this).filter(function (index) {
                    return this.name.match(/^line-\d+-vat$/);
                }).length
            )
        ) {
            elements.vat.val(
                calculator.calculate_vat(
                    elements.goods.val(),
                    calculator.get_vat_rate(elements.vat_code)
                )
            );
            event.stopPropagation();
        }
        calculator.calculate_totals();
    });


    $("table.existing_matched_transactions").on("change", "input", function (event) {
        event.stopPropagation();
        calculator.calculate_totals();
    });

    $("table.new_matched_transactions").on("change", "input", function (event) {
        event.stopPropagation();
        calculator.calculate_totals();
    });

    // on page load.  So either for editing, or errors returned when
    // trying to create
    calculator.calculate_totals();

});