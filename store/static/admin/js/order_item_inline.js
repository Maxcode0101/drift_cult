//* Recalculates order total when quantity changes in the inline formset
document.addEventListener('DOMContentLoaded', function () {
    function updateTotal() {
        let total = 0.0;

        const rows = document.querySelectorAll('.dynamic-orderitem_set');
        rows.forEach(row => {
            const priceElement = row.querySelector('td.original p');
            const quantityInput = row.querySelector('input[name$="-quantity"]');
            if (priceElement && quantityInput) {
                const priceText = priceElement.textContent.trim();
                const price = parseFloat(priceText.replace(/[^0-9.]/g, '')) || 0;
                const quantity = parseInt(quantityInput.value) || 0;
                total += price * quantity;
            }
        });

        let existingTotal = document.getElementById('live-order-total');
        if (!existingTotal) {
            const header = document.querySelector('fieldset.module.aligned h2');
            if (header) {
                existingTotal = document.createElement('div');
                existingTotal.id = 'live-order-total';
                existingTotal.style.marginTop = '10px';
                existingTotal.style.fontWeight = 'bold';
                existingTotal.style.fontSize = '1.2rem';
                header.parentNode.insertBefore(existingTotal, header.nextSibling);
            }
        }
        if (existingTotal) {
            existingTotal.innerText = `Live Order Total: $${total.toFixed(2)}`;
        }
    }

    document.addEventListener('input', function (event) {
        if (event.target.name && event.target.name.includes('-quantity')) {
            updateTotal();
        }
    });

    updateTotal(); // Initial run
});
