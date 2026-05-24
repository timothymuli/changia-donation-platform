import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    return (
        <div style={{ maxWidth: "800px", margin: "50px auto", padding: "20px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <h2>Welcome back, {user ? user.username : "User"}!</h2>
                <button
                    onClick={handleLogout}
                    style={{ padding: "10px 20px", backgroundColor: "red", color: "white", border: "none", cursor: "pointer" }}
                >
                    Logout
                </button>
            </div>
            <div style={{ marginTop: "30px" }}>
                <h3>Quick Actions</h3>
                <button
                    onClick={() => navigate("/campaigns")}
                    style={{ padding: "10px 20px", backgroundColor: "#008000", color: "white", border: "none", cursor: "pointer", marginRight: "10px" }}
                >
                    My Campaigns
                </button>
                <button
                    onClick={() => navigate("/donate")}
                    style={{ padding: "10px 20px", backgroundColor: "#0000FF", color: "white", border: "none", cursor: "pointer" }}
                >
                    Donate to a Campaign
                </button>
            </div>
        </div>
    );
};

export default Dashboard;