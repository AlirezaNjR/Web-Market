function sum_cart_total_price(number) {
  var total = document.getElementById("cart-total-price");
  var total_p_post = document.getElementById("total_price_plus_post");
  total.innerHTML = Number(total.innerHTML) + number;
  total_p_post.innerHTML = Number(total.innerHTML);
}

function difference_cart_total_price(number) {
  var total = document.getElementById("cart-total-price");
  var total_p_post = document.getElementById("total_price_plus_post");
  total.innerHTML = Number(total.innerHTML) - number;
  total_p_post.innerHTML = Number(total.innerHTML);
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

//! Delete From Cart Ajax Func
const CartDeleteBtnList = document.getElementsByClassName("cart-delete-btn");

for (const btn of CartDeleteBtnList) {
  btn.addEventListener("click", function (e) {
    e.preventDefault();
    let id = btn.getAttribute("data-id");
    $.ajax({
      url: "/Api/V1/Cart/Delete/" + id.toString() + "/",
      type: "DELETE",
      dataType: "json",
      data: "",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"), // don't forget to include the 'getCookie' function
      },
      success: (data) => {
        let parent = btn.parentNode.parentNode.parentNode;

        var quantity = document.getElementById("cart_item_count");
        quantity.innerHTML = quantity.innerHTML - 1;
        difference_cart_total_price(btn.getAttribute("data-price"));
        parent.remove();
      },
      error: (error) => {
        console.log(error);
      },
    });
  });
}

//! Add To Cart Ajax Func
const AddToCartBtn = document.getElementById("add_to_cart");
if (AddToCartBtn != null) {
  AddToCartBtn.addEventListener("click", function (e) {
    {
      e.preventDefault();

      $.ajax({
        url: "/Api/V1/Cart/Add/",
        type: "post",
        datetype: "json",
        data: {
          color: document.getElementById("color_id").value,
          quantity: document.getElementById("quantity_id").value,
          size: document.getElementById("size_id").value,
          product: document.getElementById("product_id").value,
          csrfmiddlewaretoken: getCookie("csrftoken"),
        },
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        success: (data) => {
          var OpenPanel = document.getElementById("open-panel");
          OpenPanel.innerHTML += `
                    <div class="item-in-cart clearfix">
                        <div class="image">
                            <img src="${data["Banner"]}" 
                            width="124" height="124"
                            alt="cart item" />
                        </div>
                        <div class="desc">
                            <strong><a 
							href="Product/${document.getElementById("product_id").value}/Detail/"> 
							${document.getElementById("product_name").innerHTML} </a></strong>
                            <span class="light-clr qty">
                                سایز : ${
                                  document.getElementById("size_id").value
                                }
                                &nbsp;
                            </span>
                            <span class="light-clr qty">
                                رنگ : ${
                                  document.getElementById("color_id").value
                                }
                                &nbsp;
                            </span>
                            <span class="light-clr qty">
                                تعداد : ${
                                  document.getElementById("quantity_id").value
                                }
                                &nbsp;
                                <a href="/Cart/Delete/?id=${
                                  data["Item_Id"]
                                }&rd=Product/${
            document.getElementById("product_id").value
          }/Detail/"
								class="icon-remove-sign cart-delete-btn" title="Remove Item" data-id="${
                  document.getElementById("product_id").value
                }" 
                                data-price="${
                                  document.getElementById("price").innerHTML *
                                  document.getElementById("quantity_id").value
                                }"></a>
                            </span>
                        </div>
                        <div class="price">
                            <strong> ${
                              document.getElementById("price").innerHTML *
                              document.getElementById("quantity_id").value
                            } </strong>
                        </div>
                    </div>`;
          var quantity = document.getElementById("cart_item_count");
          quantity.innerHTML = Number(quantity.innerHTML) + 1;
          var item_price =
            document.getElementById("price").innerHTML *
            document.getElementById("quantity_id").value;
          sum_cart_total_price(Number(item_price));
          try {
            document.getElementById("no_item").remove();
            document
              .getElementById("proceed")
              .setAttribute("style", "display:block;");
          } catch {
            null;
          }
        },
        error: (error) => {
          location.reload();
          document.appendChild(
            `
			<div class="alert alert-danger in fade">
			<button type="button" class="close" data-dismiss="alert">&times;</button>
				{{message}}
			</div> 
			`
          );
          console.log(error);
        },
      });
    }
  });
}

//! Delete Product Image Func
var DeleteProductImgBtns =
  document.getElementsByClassName("delete_product_img");
for (const btn of DeleteProductImgBtns) {
  btn.addEventListener("click", function (e) {
    e.preventDefault();
    let id = btn.getAttribute("data-id");
    $.ajax({
      url: `/Api/V1/Product/Image/${id}/Delete/`,
      type: "DELETE",
      dataType: "json",

      headers: {
        "X-CSRFTOKEN": getCookie("csrftoken"),
        "X-Requested-With": "XMLHttpRequest",
      },

      success: (data) => {
        btn.parentNode.remove();
        document.appendChild(
          `
			<div class="alert alert-success in fade">
				<button type="button" class="close" data-dismiss="alert">&times;</button>
				{{message}}
			</div> 
			`
        );
      },
      error: (error) => {
        console.log(error);
      },
    });
  });
}

//! New Comment for blog Post ajax func
var AddCommentBtn = document.getElementById("add-comment");
if (AddCommentBtn != null) {
  AddCommentBtn.addEventListener("click", function (e) {
    var datetime = new persianDate();
    e.preventDefault();
    $.ajax({
      url: `/Blog/${AddCommentBtn.getAttribute("data-id")}/Detail/`,
      type: "post",
      datetype: "json",
      data: {
        name: document.getElementById("author").value,
        text: document.getElementById("comment").value,
        email: document.getElementById("email").value,
        csrfmiddlewaretoken: getCookie("csrftoken"),
      },
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      success: (data) => {
        var CommentsBox = document.getElementById("comments-container");
        console.log(CommentsBox);
        CommentsBox.innerHTML += `<div class="single-comment clearfix">
					<div class="avatar-container">
						<img src="/Static/images/user-96.png" alt="avatar" class="avatar" width="184"
							height="184" />
					</div>
					<div class="comment-content">
						<div class="comment-inner">
							<cite class="author-name">
								${document.getElementById("author").value}
							</cite>
							<div class="metadata">
									${datetime.toLocale("en").format("HH:mm:ss - YYYY/MM/DD")}/ <a href="#">پاسخ</a>
							</div>
							<div class="comment-text">
								<p> ${document.getElementById("comment").value} </p>
							</div>
						</div>
					</div>
				</div>`;
			document.getElementById('comment-count').innerHTML = Number(document.getElementById('comment-count').innerHTML) + 1;
			},
      error: (error) => {},
    });
  });
}
