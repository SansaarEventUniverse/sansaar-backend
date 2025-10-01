from domain.session_model import Session


class CreateSessionService:
    def execute(self, user, ip_address=None, user_agent=None):
        """Create a new session for user"""
        # Parse device info from user agent
        device_type, browser, os = self._parse_user_agent(user_agent)
        
        session = Session.objects.create(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            device_type=device_type,
            browser=browser,
            os=os
        )
        
        return session

    def _parse_user_agent(self, user_agent):
        """Parse user agent string to extract device info"""
        if not user_agent:
            return None, None, None
        
        user_agent_lower = user_agent.lower()
        
        # Device type
        if 'mobile' in user_agent_lower or 'android' in user_agent_lower or 'iphone' in user_agent_lower:
            device_type = 'Mobile'
        elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
            device_type = 'Tablet'
        else:
            device_type = 'Desktop'
        
        # Browser
        if 'chrome' in user_agent_lower:
            browser = 'Chrome'
        elif 'firefox' in user_agent_lower:
            browser = 'Firefox'
        elif 'safari' in user_agent_lower:
            browser = 'Safari'
        elif 'edge' in user_agent_lower:
            browser = 'Edge'
        else:
            browser = 'Unknown'
        
        # OS
        if 'windows' in user_agent_lower:
            os = 'Windows'
        elif 'mac' in user_agent_lower:
            os = 'macOS'
        elif 'linux' in user_agent_lower:
            os = 'Linux'
        elif 'android' in user_agent_lower:
            os = 'Android'
        elif 'ios' in user_agent_lower or 'iphone' in user_agent_lower or 'ipad' in user_agent_lower:
            os = 'iOS'
        else:
            os = 'Unknown'
        
        return device_type, browser, os
