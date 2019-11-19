# 生成token验证
class AdminUser(Base):
    __tablename__ = 'admin_user'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    role_id = Column(INTEGER(11), nullable=False)
    company_id = Column(INTEGER(11))

    def add_admin(self, username, password, role_id):
        self.username = username
        self.password = password
        self.role_id = role_id

    def to_dict(self):
        column_name_list = [
            value[0] for value in self._sa_instance_state.attrs.items()
        ]
        return dict(
            (column_name, getattr(self, column_name, None)) \
            for column_name in column_name_list
        )

    @staticmethod
    def generate_auth_token(key_data, expiration=36000):
        key_data = base64.encodebytes(key_data)
        key_data = str(key_data, encoding="utf-8")

        return S_JMQ.dumps(key_data)

    @staticmethod
    def verify_auth_token(token):
        session = sessionmaker(engine)
        mysql_connection = session()

        try:
            data = S_JMQ.loads(token)
            print("data====")
            print(data)
            key_data = bytes(data, encoding="utf-8")
            key_data = base64.decodebytes(key_data)
            user_info_bytes = ENCRY_UTIL.decrypt(key_data)
            user_info = user_info_bytes.decode('utf-8')
            print("user_info========")
            print(user_info)
        except SignatureExpired:
            mysql_connection.close()
            return 1  # valid token, but expired
        except BadSignature:
            mysql_connection.close()
            return None  # invalid token
        admin_user = mysql_connection.query(AdminUser).filter_by(username=user_info
                                                                 .split("&")[0]) \
            .first()
        print("admin_user===")
        mysql_connection.close()
        print(admin_user)
        return admin_user
