document.addEventListener('DOMContentLoaded', function () {
    const claimLinks = document.querySelectorAll('.claim-link');

    claimLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            const claimId = this.getAttribute('data-claim-id');
            showClaimModal(claimId);
        });
    });

    function showClaimModal(claimId) {
        //calling the claim api
         fetch(`/claims/${claimId}`)
            .then(response => response.json())
            .then(data => {
                const modal = document.createElement('div');
                modal.classList.add('modal', 'fade');
                modal.setAttribute('tabindex', '-1');
                modal.setAttribute('role', 'dialog');
                const hasImage = data.item_image_url && data.item_image_url.trim() !== '';
                modal.innerHTML = `
                    <div class="modal-dialog" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Claim ${data.claim_id} Details</h5>
                                <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <div class="modal-body">
                                <img src="${data.image_url}" class="img-fluid" alt="Claim Image">
                                <p>${data.additional_information}</p>
                            </div>
                            ${hasImage ? `<img src="${data.item_image_url}" class="img-fluid" alt="Item Image">` : ''}
                             <p><strong>Item Name:</strong> ${data.item_name}</p>
                            <p><strong>Description:</strong> ${data.item_description}</p>
                            <p><strong>Category:</strong> ${data.item_category}</p>
                            <p><strong>Status:</strong> ${data.item_status}</p>
                            <p><strong>Date Reported:</strong> ${data.date_reported}</p>
                            <p><strong>User Name:</strong> ${data.user_name}</p>
                            <p><strong>User Email:</strong> ${data.user_email}</p>
                            <p><strong>User Phone:</strong> ${data.user_phone}</p>
                            <p><strong>Color:</strong> ${data.item_color}</p>
                            <p><strong>Brand:</strong> ${data.item_brand}</p>
                            <p><strong>Date Lost/Found:</strong> ${data.date_lost_found}</p>
                            <p><strong>Location Lost/Found:</strong> ${data.location_lost_found}</p>
                            <p><strong>Claim Description:</strong> ${data.claim_description}</p>
                        </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
                `;
                document.body.appendChild(modal);
                const bootstrapModal = new bootstrap.Modal(modal);
                bootstrapModal.show();
                modal.addEventListener('hidden.bs.modal', function () {
                    document.body.removeChild(modal);
                });
            })
            .catch(error => {
                console.error('Error fetching claim details:', error);
            });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const header = document.querySelector('.fixed-header');
    let lastScrollTop = 0;

    window.addEventListener('scroll', function () {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > lastScrollTop) {
            header.style.top = '-80px';
        } else {
            header.style.top = '0';
        }

        lastScrollTop = scrollTop;
    });
});



