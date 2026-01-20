/**
 * Access Code Verification Endpoint
 * Verifierar åtkomstkod för Efecte-dokumentationen
 */

const crypto = require('crypto');

// Tidskonstant jämförelse för att undvika timing-attacker
function secureCompare(a, b) {
    if (!a || !b) return false;
    if (a.length !== b.length) return false;
    return crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b));
}

module.exports = async (req, res) => {
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');

    // Handle OPTIONS (CORS preflight)
    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    // Endast POST tillåtet
    if (req.method !== 'POST') {
        return res.status(405).json({
            success: false,
            message: 'Endast POST tillåtet'
        });
    }

    try {
        const { code } = req.body || {};

        if (!code) {
            return res.status(400).json({
                success: false,
                message: 'Ingen kod angiven'
            });
        }

        const correctCode = process.env.ACCESS_CODE;

        if (!correctCode) {
            console.error('ACCESS_CODE environment variable not set');
            return res.status(500).json({
                success: false,
                message: 'Serverfel - kontakta administratör'
            });
        }

        // Verifiera koden med tidskonstant jämförelse
        const isValid = secureCompare(code, correctCode);

        if (isValid) {
            // Generera en sessionstoken
            const sessionToken = crypto.randomBytes(32).toString('hex');
            const timestamp = Date.now();

            // Skapa en signerad token (giltig i 24 timmar)
            const secret = process.env.UPDATE_API_KEY || 'session-secret';
            const message = `${sessionToken}:${timestamp}`;
            const hmac = crypto.createHmac('sha256', secret);
            hmac.update(message);
            const signature = hmac.digest('hex');

            return res.status(200).json({
                success: true,
                message: 'Inloggning lyckades',
                token: `${sessionToken}:${timestamp}:${signature}`,
                expires: timestamp + (24 * 60 * 60 * 1000) // 24 timmar
            });
        }

        return res.status(401).json({
            success: false,
            message: 'Fel kod'
        });

    } catch (error) {
        console.error('Verification error:', error);

        return res.status(500).json({
            success: false,
            message: 'Serverfel'
        });
    }
};
