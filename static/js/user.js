window.onload = async function () {
  const access_token = localStorage.getItem("access_token"); //Token value required upon request

  // if (access_token) {
  //     let temp_html = `<a onclick="logOut()" style="text-decoration: none">로그 아웃</a>`
  //     $('#user-bar').append(temp_html);
  // } else {
  //     let temp_html = `<a href="/user/signin" style="text-decoration: none">로그인 하러가기</a>`
  //     $('#user-bar').append(temp_html);
  // }
  //     if (window.location.href === `${backend_base_url}/user/page`) {
  //         const token = localStorage.getItem('access_token')  //요청시 필요한 토큰 값
  //         if (!token) {
  //             alert('로그인 후 이용해주세요.')
  //             window.location.href = '/store/goods/list';
  //         }
  //         const response = await fetch(`${backend_base_url}/user/my-page`, {
  //             headers: {
  //                 'content-type': 'application/json',
  //                 "Authorization": `Bearer ${token}`,
  //             },
  //             method: 'GET',
  //         });
  //         $('#store_info').empty();
  //         $('#user_info').empty();
  //         let response_json = await response.json()
  //         let email = response_json['user_info']['email'];
  //         let nickname = response_json['user_info']['nickname'];
  //         let profile_image = response_json['user_info']['profile_image'];
  //         let temp_html = `
  //                                     <h2>내 정보</h2>
  //                                     ${profile_image}<br>
  //                                     ${email}<br>
  //                                     ${nickname}<br>
  //                                     현재 비밀번호 : <input id='origin_password' type="password"><br>
  //                                     새 비밀번호 : <input id='password' type="password"><br>
  //                                     새 비밀번호 : <input id='password2' type="password"><br>
  //                                     <button onclick="changePassword()">확인</button>
  // <!--                                    <button onclick="userDelete()">탈퇴</button>-->
  //                                     <br>
  //                                     `;
  //         $('#user_info').append(temp_html);
  //         if (response_json['store_info']) {
  //             let address = response_json['store_info']['address'];
  //             let introduce = response_json['store_info']['introduce'];
  //             let name = response_json['store_info']['name'];
  //             let phone = response_json['store_info']['phone'];
  //             let temp_html = `
  //                                     <h2>상점 정보</h2>
  //                                     ${address}<br>
  //                                     ${introduce}<br>
  //                                     ${name}<br>
  //                                     ${phone}<br>
  //                                     <br>
  //                                     `;
  //             $('#store_info').append(temp_html);
  //         }
  //     }
  const params = new URLSearchParams(window.location.search);
  const code = params.get("code");

  if (code) {
    // Google decodes the encoded URL and stores it in localStorage.
    const encodeCode = code;
    const decodeCode = decodeURIComponent(encodeCode.replace(/\+/g, " "));
    await googleLoginApi(decodeCode); // Call the googleLoginApi function
  } // Check Google login and check token
};

async function logOut() {
  let _confirm = confirm("On the connected device\nDo you want to log out?");
  if (_confirm) {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("store_id");
    localStorage.removeItem("chat_user");
    localStorage.removeItem("store_name");
    localStorage.removeItem("image");
    alert("log out!");
    window.location.href = "/user/signin";
  }
}

async function changePassword() {
  const access_token = localStorage.getItem("access_token"); //Token value required upon request
  let data = {
    origin_password: document.getElementById("origin_password").value,
    password: document.getElementById("password").value,
    password2: document.getElementById("password2").value,
  };
  const response = await fetch(`${backend_base_url}/user/my-page`, {
    headers: {
      "content-type": "application/json",
      Authorization: `Bearer ${access_token}`,
    },
    body: JSON.stringify(data),
    method: "PATCH",
  });
  let response_json = await response.json();
  console.log(response_json);
  if (response.ok) {
    alert(response_json["message"]);
  } else {
    if (response_json["message"]) {
      if (response_json["message"].includes("8자")) {
        alert("Please write your password with at least 8 characters.");
      } else {
        alert(response_json["message"]);
      }
    }
  }
}

async function logIn(data = null) {
  if (!data) {
    data = {
      email: document.getElementById("email").value,
      password: document.getElementById("password").value,
    };
  }
  const response = await fetch(`${backend_base_url}/user/signin`, {
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify(data),
    method: "POST",
  });
  let response_json = await response.json();
  if (response.ok) {
    if (response_json["token"]["access"]) {
      localStorage.setItem("access_token", response_json["token"]["access"]);
      localStorage.setItem("refresh_token", response_json["token"]["refresh"]);
      localStorage.setItem("user_id", response_json["user_id"]);
      localStorage.setItem("user_name", response_json["user_name"]);
      localStorage.setItem(
        "origin_store_name",
        response_json["origin_store_name"]
      );
      localStorage.setItem("image", response_json["image"]);
      localStorage.setItem("email", response_json["email"]);
      if (response_json["store_id"]) {
        localStorage.setItem("store_id", response_json["store_id"]);
      }
    }
    window.location.href = "/store/goods/list";
  } else if (response_json["message"] || response_json["detail"]) {
    let message = response_json["message"];
    let detail = response_json["detail"];
    if (message) {
      document.getElementById("error_msg").innerText =
        "The username or password do not match.";
    } else if (detail) {
      document.getElementById("error_msg").innerText =
        "The username or password do not match.";
    }
    document.getElementById("error_msg").style.display = "block";
  }
}

async function signUp() {
  const params = new URLSearchParams(window.location.search);
  const user_type = params.get("user_type");
  let data = {
    category: user_type,
    email: document.getElementById("email").value,
    code: document.getElementById("code").value,
    password: document.getElementById("password").value,
    password2: document.getElementById("password2").value,
  };
  // const image = document.getElementById("image")
  if (user_type === "2") {
    let seller_data = {
      name: document.getElementById("name").value,
      nickname: document.getElementById("name").value,
      phone: document.getElementById("phone").value,
      address: document.getElementById("address").value,
      sub_address: document.getElementById("sub_address").value,
      company_number: document.getElementById("company_number").value,
      introduce: document.getElementById("introduce").value,
    };
    data = Object.assign({}, data, seller_data);
  } else {
    let basic_user_data = {
      nickname: document.getElementById("nickname").value,
    };
    data = Object.assign({}, data, basic_user_data);
  }
  const response = await fetch(`${backend_base_url}/user/signup`, {
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify(data),
    method: "POST",
  });
  let response_json = await response.json();
  if (response.ok) {
    await logIn(data);
  } else if (response_json["message"]) {
    message = response_json["message"];
    document.getElementById("error_msg").innerText = message;
    document.getElementById("error_msg").style.display = "block";
  }
}

function copytoclipboard(val) {
  var t = document.createElement("textarea");
  document.body.appendChild(t);
  t.value = val;
  t.select();
  document.execCommand("copy");
  document.body.removeChild(t);
}
function inappbrowserout() {
  copytoclipboard(window.location.href);
  alert(
    'The URL address has been copied.\n\nWhen Safari opens, touch and hold the address bar, then press "Paste and Move" to use it normally.'
  );
  location.href = "x-web-search://?";
}

async function googleUrl() {
  const response = await fetch(`${backend_base_url}/user/social`, {
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify({ social: "google" }),
    method: "POST",
  });
  let response_json = await response.json();
  var userAgent = navigator.userAgent;
  if (response.ok) {
    const response_url = response_json.url;
    var target_url = response_url;
    if (userAgent.match(/kakao/i)) {
      window.location.href =
        "kakaotalk://web/openExternal?url=" + encodeURIComponent(target_url);
    } else if (userAgent.match(/naver/i)) {
      if (userAgent.match(/iphone|ipad|ipod/i)) {
        var mobile = document.createElement("meta");
        mobile.name = "viewport";
        mobile.content =
          "width=device-width, initial-scale=1, shrink-to-fit=no, user-scalable=no, minimal-ui";
        document.getElementsByTagName("head")[0].appendChild(mobile);
        //Force setting of Notosan font
        var fonts = document.createElement("link");
        fonts.href =
          "https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100;300;400;500;700;900&display=swap";
        document.getElementsByTagName("head")[0].appendChild(fonts);
        document.body.innerHTML =
          "<style>body{margin:0;padding:0;font-family: 'Noto Sans KR', sans-serif;overflow: hidden;height: 100%;}</style><h2 style='padding-top:50px; text-align:center;font-family: 'Noto Sans KR', sans-serif;'>인앱브라우저 호환문제로 인해<br />Safari로 접속해야합니다.</h2><article style='text-align:center; font-size:17px; word-break:keep-all;color:#999;'>아래 버튼을 눌러 Safari를 실행해주세요<br />Safari가 열리면, 주소창을 길게 터치한 뒤,<br />'붙여놓기 및 이동'을 누르면<br />정상적으로 이용할 수 있습니다.<br /><br /><button onclick='inappbrowserout();' style='min-width:180px;margin-top:10px;height:54px;font-weight: 700;background-color:#31408E;color:#fff;border-radius: 4px;font-size:17px;border:0;'>Safari로 열기</button></article><img style='width:70%;margin:50px 15% 0 15%' src='https://tistory3.daumcdn.net/tistory/1893869/skin/images/inappbrowserout.jpeg' />";
      } else {
        location.href =
          "intent://" +
          target_url.replace(/https?:\/\//i, "") +
          "#Intent;scheme=http;package=com.android.chrome;end";
      }
    } else {
      window.location.href = response_url;
    }
  } else if (response_json["message"]) {
    message = response_json["message"];
    alert(message);
  }
}

// Send to Google login data server
async function googleLoginApi(decodeCode) {
  const response = await fetch(`${backend_base_url}/user/google`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ code: decodeCode }),
  });
  const response_json = await response.json();

  if (response.status === 200) {
    localStorage.setItem("access_token", response_json.access);
    localStorage.setItem("refresh_token", response_json.refresh);
    localStorage.setItem("user_id", response_json["user_id"]);
    localStorage.setItem("user_name", response_json["user_name"]);
    localStorage.setItem(
      "origin_store_name",
      response_json["origin_store_name"]
    );
    localStorage.setItem("image", response_json["image"]);
    localStorage.setItem("email", response_json["email"]);
    if (response_json["store_id"]) {
      localStorage.setItem("store_id", response_json["store_id"]);
    }

    if (response_json["is_first"]) {
      localStorage.setItem("is_first", response_json["is_first"]);
    }
    window.location.href = "/store/goods/list";
  } else if (response_json.status == 400) {
    alert(response_json["error"]);
  } else {
    alert(response_json["error"]);
    window.history.back();
  }
}

async function sellerSignUp() {
  let data = {
    name: document.getElementById("name").value,
    phone: document.getElementById("phone").value,
    address: document.getElementById("address").value,
    sub_address: document.getElementById("sub_address").value,
    company_number: document.getElementById("company_number").value,
    introduce: document.getElementById("introduce").value,
    user_id: localStorage.getItem("user_id"), //Token value required upon request
  };
  const response = await fetch(`${backend_base_url}/user/seller-signup`, {
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify(data),
    method: "POST",
  });
  let response_json = await response.json();
  if (response.ok) {
    localStorage.setItem("user_id", response_json["user_id"]);
    localStorage.setItem("user_name", response_json["user_name"]);
    localStorage.setItem(
      "origin_store_name",
      response_json["origin_store_name"]
    );
    localStorage.setItem("image", response_json["image"]);
    localStorage.setItem("email", response_json["email"]);
    if (response_json["store_id"]) {
      localStorage.setItem("store_id", response_json["store_id"]);
    }
    localStorage.removeItem("is_first");

    window.location.href = "/store/goods/list";
  } else if (response_json["message"]) {
    message = response_json["message"];
    document.getElementById("error_msg").innerText = message;
    document.getElementById("error_msg").style.display = "block";
  }
}

async function sendEmailCode() {
  let email = document.getElementById("email").value;
  if (!email) {
    document.getElementById("error_msg").innerText = "Please enter your e-mail.";
    document.getElementById("error_msg").style.display = "block";
    return false;
  }
  let data = {
    email: email,
  };
  startEmailTimer();
  const response = await fetch(`${backend_base_url}/user/send-email`, {
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify(data),
    method: "POST",
  });
  // timer
  let response_json = await response.json();
  if (response.ok) {
    document.getElementById("email").readOnly = true;
  } else if (response_json["message"]) {
    message = response_json["message"];
    document.getElementById("error_msg").innerText = "Please enter your e-mail.";
    document.getElementById("error_msg").style.display = "block";
  }
}

function startTimer(duration, display) {
  var timer = duration,
    minutes,
    seconds;
  var interval = setInterval(function () {
    minutes = parseInt(timer / 60, 10);
    seconds = parseInt(timer % 60, 10);

    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    display.innerText = minutes + ":" + seconds;

    if (--timer < 0) {
      clearInterval(interval);
      display.innerText = "certify"; // Text to display when timer ends
      document.getElementById("email").readOnly = false;
      document.getElementById("email_send_btn").onclick = function () {
        sendEmailCode();
      };
    }
  }, 1000);
}

// Timer start function
function startEmailTimer() {
  var threeMinutes = 60 * 3, // 3 minutes
    display = document.getElementById("email_send_btn");
  document.getElementById("email_send_btn").onclick = null;
  startTimer(threeMinutes, display);
}

async function checkEmailCode() {
  let data = {
    email: document.getElementById("email").value,
    code: document.getElementById("code").value,
  };
  const response = await fetch(`${backend_base_url}/user/check-email`, {
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify(data),
    method: "POST",
  });
  let response_json = await response.json();
  if (response.ok) {
    localStorage.setItem("is_checked", response_json["is_checked"]);
    alert(response_json["message"]);
  } else if (response_json["message"]) {
    message = response_json["message"];
    alert(message);
  }
}

async function myPage() {
  const access_token = localStorage.getItem("access_token"); //Token value required when requesting
  if (access_token) {
    window.location.href = `${backend_base_url}/user/page`;
  } else {
    alert("Please use after logging in.");
    // window.location.href = '/store/goods-list'
  }
}

async function storeSetting() {
  const access_token = localStorage.getItem("access_token"); //Token value required when requesting

  if (access_token) {
    window.location.href = `${backend_base_url}/store/setting`;
  } else {
    alert("Please use after logging in.");
    // window.location.href = '/store/goods-list'
  }
}

async function sellerHome() {
  const access_token = localStorage.getItem("access_token"); //Token value required when requesting
  if (access_token) {
    window.location.href = `${backend_base_url}/user/page`;
  } else {
    alert("Please use after logging in.");
    // window.location.href = '/store/goods-list'
  }
}

async function findPassword() {
  let data = {
    email: document.getElementById("email").value,
    code: document.getElementById("code").value,
    password: document.getElementById("password").value,
    password2: document.getElementById("password2").value,
  };

  const response = await fetch(`${backend_base_url}/user/my-page`, {
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify(data),
    method: "POST",
  });

  let response_json = await response.json();

  console.log(response_json);
  if (response.ok) {
    alert(response_json["message"]);
    window.location.href = "/user/signin";
  } else if (response_json["message"]) {
    message = response_json["message"];
    document.getElementById("error_msg").innerText = message;
    document.getElementById("error_msg").style.display = "block";
  }
}
