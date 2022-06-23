"use strict";
var KTDatatablesAdvancedColumnRendering = function() {

	var init = function() {
		var table = $('#kt_datatable');

		// begin first table
		table.DataTable({
			language: {
            url: '//cdn.datatables.net/plug-ins/1.11.3/i18n/ru.json'
        },
			responsive: true,
			paging: true,
			columnDefs: [
				{
					targets: 1,
					render: function(data, type, full, meta) {
						return '<a class="text-dark-50 text-hover-primary" href="mailto:' + data + '">' + data + '</a>';
					},
				},
			],
		});

		$('#kt_datatable_search_status').on('change', function() {
			datatable.search($(this).val().toLowerCase(), 'Status');
		});

		$('#kt_datatable_search_type').on('change', function() {
			datatable.search($(this).val().toLowerCase(), 'Type');
		});

		$('#kt_datatable_search_status, #kt_datatable_search_type').selectpicker();
	};

	return {

		//main function to initiate the module
		init: function() {
			init();
		}
	};
}();

jQuery(document).ready(function() {
	KTDatatablesAdvancedColumnRendering.init();
});
