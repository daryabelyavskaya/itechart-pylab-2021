var modal = $modal({
    title: 'Choose filter',
    content: '<p></p>',
    footerButtons: [
      { class: 'btn btn__cancel', text: 'Отмена', handler: 'modalHandlerCancel' },
      { class: 'btn btn__ok', text: 'ОК', handler: 'modalHandlerOk' }
    ]
  });