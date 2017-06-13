# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Enum, Index, Integer, Numeric, String, Table, Text, text
from sqlalchemy.ext.declarative import declarative_base
from jsonpickle import handlers


Base = declarative_base()
metadata = Base.metadata


t_atualizar = Table(
    'atualizar', metadata,
    Column('aviso', Text),
    Column('bckemail', String(3), server_default=text("'nao'")),
    Column('bckemailend', String(255), server_default=text("'seu@email.com.br'")),
    Column('avisoatrazo', String),
    Column('enviarsolic', String(3), server_default=text("'sim'")),
    Column('avisocinco', String),
    Column('enviamsgemail', String(3), server_default=text("'sim'")),
    Column('pgnight', String),
    Column('pgreparo', String),
    Column('contrato', String),
    Column('cartacob', String),
    Column('recibo', String),
    Column('bloqradius', Enum('sim', 'nao'), nullable=False, server_default=text("'sim'")),
    Column('pgcorte', Enum('nao', 'rad', 'ssh'), nullable=False, server_default=text("'rad'")),
    Column('tbloqradius', Enum('pool', 'mangle', 'list'), server_default=text("'list'")),
    Column('tipoficha', Enum('int', 'man'), server_default=text("'int'")),
    Column('fichacham', String),
    Column('pbloqradius', Enum('pool', 'list'), server_default=text("'list'"))
)


class Backup(Base):
    __tablename__ = 'backup'

    id = Column(Integer, primary_key=True)
    data = Column(String(255), nullable=False)
    descricao = Column(String(255))
    caminho = Column(String(255), nullable=False)
    tipo = Column(String(3), server_default=text("'bz2'"))


class Na(Base):
    __tablename__ = 'nas'

    id = Column(Integer, primary_key=True)
    nasname = Column(String(128), nullable=False, index=True)
    shortname = Column(String(32))
    type = Column(String(30), server_default=text("'other'"))
    ports = Column(Integer)
    secret = Column(String(60), nullable=False, server_default=text("'secret'"))
    server = Column(String(64))
    community = Column(String(50))
    description = Column(String(200), server_default=text("'RADIUS Client'"))
    tipo = Column(String(2), server_default=text("'pc'"))
    maxclientes = Column(Integer, server_default=text("'1000'"))
    sshativo = Column(Enum('sim', 'nao'), nullable=False, server_default=text("'sim'"))
    portassh = Column(String(5), nullable=False, server_default=text("'22'"))
    senha = Column(String(255))
    ftpativo = Column(Enum('sim', 'nao'), server_default=text("'nao'"))
    endereco = Column(String(255))
    numero = Column(String(20))
    bairro = Column(String(255))
    cidade = Column(String(255))
    cep = Column(String(9))
    estado = Column(String(2))
    complemento = Column(String(255))
    idplaca = Column(Integer, server_default=text("'1'"))
    cidade_ibge = Column(String(16))
    mb_instalados = Column(Integer, server_default=text("'99'"))
    coordenadas = Column(String(50))


class Radacct(Base):
    __tablename__ = 'radacct'

    radacctid = Column(BigInteger, primary_key=True)
    acctsessionid = Column(String(64), nullable=False, index=True, server_default=text("''"))
    acctuniqueid = Column(String(32), nullable=False, unique=True, server_default=text("''"))
    username = Column(String(64), nullable=False, index=True, server_default=text("''"))
    groupname = Column(String(64), nullable=False, server_default=text("''"))
    realm = Column(String(64), server_default=text("''"))
    nasipaddress = Column(String(15), nullable=False, index=True, server_default=text("''"))
    nasportid = Column(String(15))
    nasporttype = Column(String(32))
    acctstarttime = Column(DateTime, index=True)
    acctstoptime = Column(DateTime, index=True)
    acctsessiontime = Column(Integer, index=True)
    acctauthentic = Column(String(32))
    connectinfo_start = Column(String(50))
    connectinfo_stop = Column(String(50))
    acctinputoctets = Column(BigInteger)
    acctoutputoctets = Column(BigInteger)
    calledstationid = Column(String(50), nullable=False, server_default=text("''"))
    callingstationid = Column(String(50), nullable=False, server_default=text("''"))
    acctterminatecause = Column(String(32), nullable=False, server_default=text("''"))
    servicetype = Column(String(32))
    framedprotocol = Column(String(32))
    framedipaddress = Column(String(15), nullable=False, index=True, server_default=text("''"))
    acctstartdelay = Column(Integer)
    acctstopdelay = Column(Integer)
    xascendsessionsvrkey = Column(String(10))


class Radcheck(Base):
    __tablename__ = 'radcheck'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True)
    attribute = Column(String(64), nullable=False)
    op = Column(String(2), nullable=False, server_default=text("'=='"))
    value = Column(String(253), nullable=False)
    ativo = Column(Enum('s', 'n'), server_default=text("'s'"))
    login = Column(String(64), index=True)
    tipo = Column(Enum('log', 'mac'), nullable=False, server_default=text("'log'"))


class Radgroupcheck(Base):
    __tablename__ = 'radgroupcheck'

    id = Column(Integer, primary_key=True)
    groupname = Column(String(64), nullable=False, index=True, server_default=text("''"))
    attribute = Column(String(64), nullable=False, server_default=text("''"))
    op = Column(String(2), nullable=False, server_default=text("'=='"))
    value = Column(String(253), nullable=False, server_default=text("''"))


class Radgroupreply(Base):
    __tablename__ = 'radgroupreply'

    id = Column(Integer, primary_key=True)
    groupname = Column(String(64), nullable=False, index=True, server_default=text("''"))
    attribute = Column(String(64), nullable=False, server_default=text("''"))
    op = Column(String(2), nullable=False, server_default=text("'='"))
    value = Column(String(253), nullable=False, server_default=text("''"))


class Radippool(Base):
    __tablename__ = 'radippool'
    __table_args__ = (
        Index('radippool_nasip_poolkey_ipaddress', 'nasipaddress', 'pool_key', 'framedipaddress'),
        Index('radippool_poolname_expire', 'pool_name', 'expiry_time')
    )

    id = Column(Integer, primary_key=True)
    pool_name = Column(String(30), nullable=False)
    framedipaddress = Column(String(15), nullable=False, index=True, server_default=text("''"))
    nasipaddress = Column(String(15), nullable=False, server_default=text("''"))
    calledstationid = Column(String(30), nullable=False)
    callingstationid = Column(String(30), nullable=False)
    expiry_time = Column(DateTime)
    username = Column(String(64), nullable=False, server_default=text("''"))
    pool_key = Column(String(30), nullable=False)


class Radpostauth(Base):
    __tablename__ = 'radpostauth'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True, server_default=text("''"))
    _pass = Column('pass', String(64), nullable=False, server_default=text("''"))
    reply = Column(String(32), nullable=False, server_default=text("''"))
    authdate = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    ip = Column(String(50))
    mac = Column(String(50))
    ramal = Column(String(50))


class Radreply(Base):
    __tablename__ = 'radreply'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True)
    attribute = Column(String(64), nullable=False)
    op = Column(String(2), nullable=False, server_default=text("'='"))
    value = Column(String(253), nullable=False)
    login = Column(String(64), index=True)


t_radusergroup = Table(
    'radusergroup', metadata,
    Column('username', String(64), nullable=False, index=True),
    Column('groupname', String(64), nullable=False),
    Column('priority', Integer, nullable=False, server_default=text("'1'")),
    Column('login', String(64), index=True)
)


class Registro(Base):
    __tablename__ = 'registro'

    id = Column(Integer, primary_key=True)
    licenca = Column(String(255))
    validade = Column(String(50))
    data = Column(DateTime)
    chavetea = Column(String(50))


class SisAcesso(Base):
    __tablename__ = 'sis_acesso'

    idacesso = Column(Integer, primary_key=True)
    login = Column(String(255), index=True)
    sha = Column(String(255))
    ultacesso = Column(String(255))
    email = Column(String(255))
    nivel = Column(String(255))
    nome = Column(String(255))
    horario = Column(Enum('sim', 'nao'), server_default=text("'nao'"))
    tempoil = Column(String(5))
    tempofl = Column(String(5))
    ativo = Column(Enum('sim', 'nao'), server_default=text("'sim'"))
    key_onetime = Column(String(16))
    cli_grupos = Column(String(255), server_default=text("'full_clientes'"))
    sesid = Column(String(64), server_default=text("'5k0ahkfa9d9r0i6mucm0khlcdralfnf1'"))


class SisAdicional(Base):
    __tablename__ = 'sis_adicional'

    id = Column(Integer, primary_key=True)
    tipo = Column(Enum('hotspot', 'pppoe'), nullable=False, index=True, server_default=text("'hotspot'"))
    username = Column(String(64), unique=True)
    senha = Column(String(32), index=True)
    ip = Column(String(15), index=True)
    mac = Column(String(17), index=True)
    ramal = Column(String(15))
    chavetipo = Column(String(10))
    chave = Column(String(255))
    login = Column(String(64), index=True)
    plano = Column(String(253), index=True)
    simultaneo = Column(Enum('sim', 'nao'), nullable=False, server_default=text("'nao'"))
    accesslist = Column(Enum('sim', 'nao'), nullable=False, index=True, server_default=text("'sim'"))
    bloqueado = Column(Enum('sim', 'nao'), server_default=text("'nao'"))
    telefone = Column(String(23))
    end_endereco = Column(String(255))
    end_numero = Column(String(15))
    end_complemento = Column(String(127))
    end_bairro = Column(String(127))
    end_cidade = Column(String(63))
    interface = Column(String(128), index=True)
    nome = Column(String(128))
    pool_name = Column(String(30), server_default=text("'nenhum'"))
    night = Column(Enum('sim', 'nao'), server_default=text("'nao'"))
    coordenadas = Column(String(64))
    plano_bloqa = Column(String(64), index=True, server_default=text("'nenhum'"))
    armario_olt = Column(String(96))
    porta_olt = Column(String(32))
    caixa_herm = Column(String(128))
    porta_splitter = Column(String(32))
    onu_ont = Column(String(64))
    switch = Column(String(128))


class SisBoleto(Base):
    __tablename__ = 'sis_boleto'

    id = Column(Integer, primary_key=True)
    utilizar = Column(String(10), nullable=False)
    banco = Column(String(200))
    codigo_cedente = Column(Text)
    agencia = Column(Text)
    ag_digito = Column(Text)
    conta = Column(Text)
    ct_digito = Column(Text)
    carteira = Column(Text)
    convenio = Column(Text)
    cedente = Column(Text)
    contrato = Column(Text)
    obs_linha1 = Column(Text)
    obs_linha2 = Column(Text)
    obs_linha3 = Column(Text)
    obs_linha4 = Column(Text)
    instr_linha1 = Column(Text)
    instr_linha2 = Column(Text)
    instr_linha3 = Column(Text)
    instr_linha4 = Column(Text)
    instr_linha5 = Column(Text)
    taxa = Column(String(20))
    nosso = Column(String(255))
    f2bconta = Column(String(255))
    f2bsenha = Column(String(20))
    multa = Column(String(20))
    juros = Column(String(20))
    codigo_cliente = Column(String(255))
    ponto_venda = Column(String(255))
    nosso1 = Column(String(3))
    nosso2 = Column(String(3))
    nosso3 = Column(String(9))
    constante1 = Column(String(1))
    constante2 = Column(String(1))
    byte = Column(String(1))
    token = Column(String(255))
    gateway = Column(String(5), server_default=text("'f2b'"))
    pagseguro = Column(String(255))
    pagdigital = Column(String(255))
    modalidade = Column(String(2), server_default=text("'02'"))
    paypalconta = Column(String(255))
    diasatraso = Column(Integer, server_default=text("'90'"))
    layout = Column(String(255), server_default=text("'detalhado'"))
    logosva = Column(String(3), server_default=text("'nao'"))
    instauto = Column(String(3), server_default=text("'sim'"))
    nossonumfinal = Column(String(255))
    tipo = Column(String(255))
    variacao = Column(String(5), server_default=text("'-019'"))
    localpag = Column(String(255), server_default=text("'ANTES DO VENCIMENTO EM TODOS OS BANCOS'"))
    titulo_inicial = Column(Integer)
    avalista = Column(String(255))
    desconto = Column(Numeric(12, 2), server_default=text("'0.00'"))
    tipodesc = Column(Enum('fixo', 'perc'), server_default=text("'fixo'"))
    cpf_cnpj = Column(String(50))
    esp_doc = Column(String(12))
    token_gnet = Column(String(32))
    nome = Column(String(50), server_default=text("'conta corrente'"))
    varalfa = Column(String(2), server_default=text("'aa'"))
    token_bcash = Column(String(70))
    token_pagseguro = Column(String(70))
    calc_boleto = Column(Enum('sim', 'nao'), server_default=text("'sim'"))
    last_update = Column(DateTime)
    referencia = Column(Enum('sim', 'nao'), server_default=text("'sim'"))
    transmissao = Column(String(20))
    layout_pdf = Column(String(255), server_default=text("'pdf'"))
    complemento = Column(String(2), server_default=text("'00'"))
    contra = Column(Enum('sim', 'nao'), server_default=text("'nao'"))
    cnab = Column(Enum('240', '400'), server_default=text("'400'"))
    num_remessa = Column(Integer)
    id_conta_gnet = Column(String(32))
    cliente_id_gnet = Column(String(64))
    cliente_secret_gnet = Column(String(64))
    cliente_id_teste_gnet = Column(String(64))
    cliente_secret_teste_gnet = Column(String(64))
    ocorrencia = Column(String(128))
    codbanco = Column(String(3))
    tipo_desc = Column(Enum('perc', 'fixo'), server_default=text("'fixo'"))


class SisCaixa(Base):
    __tablename__ = 'sis_caixa'

    id = Column(Integer, primary_key=True)
    usuario = Column(String(50))
    data = Column(DateTime)
    historico = Column(String(255))
    complemento = Column(String)
    entrada = Column(Numeric(12, 2))
    saida = Column(Numeric(12, 2))
    tipomov = Column(Enum('aut', 'man'), server_default=text("'aut'"))
    planodecontas = Column(String(50), server_default=text("'Outros'"))


class SisCarne(Base):
    __tablename__ = 'sis_carne'

    id = Column(Integer, primary_key=True)
    cliente = Column(String(255))
    login = Column(String(100), index=True)
    codigo = Column(String(32), index=True)
    emissao = Column(DateTime)
    parcelas = Column(Integer)
    descricao = Column(String(255))
    impresso = Column(Enum('sim', 'nao'), server_default=text("'nao'"))
    banco = Column(String(100))
    urlcarne = Column(String(255))
    urlcapa = Column(String(255))
    delcarne = Column(Integer, index=True, server_default=text("'0'"))


class SisCartahom(Base):
    __tablename__ = 'sis_cartahom'

    idhomo = Column(Integer, primary_key=True)
    login = Column(String(128), index=True)
    valor = Column(Numeric(12, 2))
    titulo = Column(Integer)
    datavenc = Column(DateTime)
    referencia = Column(String(64))
    nossonum = Column(String(64))
    processamento = Column(DateTime)
    gerourem = Column(Enum('sim', 'nao'), server_default=text("'nao'"))
    percmulta = Column(Numeric(4, 2))
    valormulta = Column(Numeric(12, 2))
    percmora = Column(Numeric(4, 2))
    valormora = Column(Numeric(12, 2))
    percdesc = Column(Numeric(4, 2))
    valordesc = Column(Numeric(12, 2))
    keyrem = Column(String(32), index=True)


t_sis_central = Table(
    'sis_central', metadata,
    Column('laycentral', String(50), nullable=False, server_default=text("'padrao'")),
    Column('altsenha', String(3), server_default=text("'nao'")),
    Column('altdados', String(3), server_default=text("'sim'")),
    Column('speed', String(3), server_default=text("'sim'")),
    Column('altlogin', String(3), server_default=text("'sim'")),
    Column('vercontrato', String(3), server_default=text("'sim'")),
    Column('batepapo', String(3), server_default=text("'sim'")),
    Column('captcha', String(3), server_default=text("'sim'")),
    Column('vercontato', String(3), server_default=text("'sim'")),
    Column('helpdesk', Enum('sim', 'nao'), nullable=False, server_default=text("'sim'")),
    Column('fsenha', Enum('senha', 'cpf', 'lcpf', 'ltseg'), server_default=text("'senha'")),
    Column('discovirtual', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('multihelp', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('envsenha', Enum('sim', 'nao'), server_default=text("'sim'")),
    Column('smssenha', Enum('sim', 'nao'), server_default=text("'sim'")),
    Column('showgraf', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('bopenchamados', Enum('sim', 'nao'), server_default=text("'nao'"))
)


class SisCliente(Base):
    __tablename__ = 'sis_cliente'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), index=True)
    email = Column(String(255))
    endereco = Column(String(255))
    bairro = Column(String(255))
    cidade = Column(String(255))
    cep = Column(String(9))
    estado = Column(String(2))
    cpf_cnpj = Column(String(20))
    fone = Column(String(50))
    obs = Column(Text)
    nascimento = Column(String(255))
    cadastro = Column(String(255))
    login = Column(String(64), unique=True)
    tipo = Column(String(10), index=True)
    night = Column(String(3), server_default=text("'nao'"))
    aviso = Column(Text)
    foto = Column(String(255))
    venc = Column(String(2), server_default=text("'01'"))
    mac = Column(String(17), index=True)
    complemento = Column(String(255))
    ip = Column(String(20), index=True)
    ramal = Column(String(255), index=True)
    rg = Column(String(255), index=True)
    isento = Column(String(3), server_default=text("'nao'"))
    celular = Column(String(50))
    bloqueado = Column(String(3), index=True, server_default=text("'nao'"))
    autoip = Column(String(3), server_default=text("'sim'"))
    automac = Column(String(3), server_default=text("'sim'"))
    conta = Column(String(11), server_default=text("'1'"))
    ipvsix = Column(String(255))
    plano = Column(String(255), index=True)
    send = Column(String(3), server_default=text("'nao'"))
    cli_ativado = Column(Enum('s', 'n'), index=True, server_default=text("'s'"))
    simultaneo = Column(String(3), server_default=text("'nao'"))
    turbo = Column(String(255), server_default=text("'nenhum'"))
    comodato = Column(String(3), server_default=text("'nao'"))
    observacao = Column(String(3), index=True, server_default=text("'nao'"))
    chavetipo = Column(String(10))
    chave = Column(String(255))
    contrato = Column(String(8), server_default=text("'87654321'"))
    ssid = Column(String(255))
    senha = Column(String(255), index=True)
    numero = Column(String(20))
    responsavel = Column(String(255))
    nome_pai = Column(String(255))
    nome_mae = Column(String(255))
    expedicao_rg = Column(String(20))
    naturalidade = Column(String(50))
    acessacen = Column(String(50), server_default=text("'sim'"))
    pessoa = Column(String(10), server_default=text("'fisica'"))
    endereco_res = Column(String(255))
    numero_res = Column(String(20))
    bairro_res = Column(String(255))
    cidade_res = Column(String(255))
    cep_res = Column(String(9))
    estado_res = Column(String(2))
    complemento_res = Column(String(255))
    desconto = Column(Numeric(12, 2), index=True, server_default=text("'0.00'"))
    acrescimo = Column(Numeric(12, 2), index=True, server_default=text("'0.00'"))
    equipamento = Column(String(20), server_default=text("'nenhum'"))
    vendedor = Column(String(255))
    nextel = Column(String(50))
    accesslist = Column(Enum('sim', 'nao'), nullable=False, index=True, server_default=text("'nao'"))
    resumo = Column(String(6), server_default=text("'032011'"))
    grupo = Column(String(50))
    codigo = Column(String(50))
    prilanc = Column(Enum('pro', 'tot'), nullable=False, server_default=text("'pro'"))
    tipobloq = Column(Enum('aut', 'man'), nullable=False, server_default=text("'aut'"))
    adesao = Column(Numeric(12, 2), server_default=text("'0.00'"))
    mbdisco = Column(Integer, nullable=False, server_default=text("'100'"))
    impsel = Column(Enum('sim', 'nao'), server_default=text("'nao'"))
    sms = Column(Enum('sim', 'nao'), server_default=text("'sim'"))
    ltrafego = Column(BigInteger, server_default=text("'0'"))
    planodown = Column(String(255), server_default=text("'nenhum'"))
    ligoudown = Column(String(6), server_default=text("'012011'"))
    statusdown = Column(Enum('on', 'off'), nullable=False, server_default=text("'off'"))
    statusturbo = Column(Enum('on', 'off'), nullable=False, server_default=text("'off'"))
    opcelular = Column(String(100), server_default=text("'nenhuma'"))
    nome_res = Column(String(255))
    coordenadas = Column(String(64))
    rem_obs = Column(DateTime)
    valor_sva = Column(Numeric(12, 2), server_default=text("'0.00'"))
    dias_corte = Column(Integer, server_default=text("'999'"))
    user_ip = Column(String(100))
    user_mac = Column(String(100))
    data_ip = Column(DateTime)
    data_mac = Column(DateTime)
    last_update = Column(DateTime)
    data_bloq = Column(DateTime)
    tags = Column(String)
    tecnico = Column(String(255))
    data_ins = Column(DateTime)
    altsenha = Column(Enum('sim', 'nao'))
    geranfe = Column(Enum('sim', 'nao'), server_default=text("'sim'"))
    mesref = Column(Enum('now', 'ant'), server_default=text("'ant'"))
    ipfall = Column(String(32))
    tit_abertos = Column(Integer, index=True)
    parc_abertas = Column(Integer, index=True)
    tipo_pessoa = Column(Integer)
    celular2 = Column(String(32))
    mac_serial = Column(String(255))
    status_corte = Column(Enum('full', 'down', 'bloq'), server_default=text("'full'"))
    plano15 = Column(String(255), server_default=text("'nenhum'"))
    pgaviso = Column(Enum('sim', 'nao'), index=True, server_default=text("'sim'"))
    porta_olt = Column(String(32))
    caixa_herm = Column(String(128))
    porta_splitter = Column(String(32))
    onu_ont = Column(String(64))
    switch = Column(String(128))
    tit_vencidos = Column(Integer, index=True)
    pgcorte = Column(Enum('sim', 'nao'), index=True, server_default=text("'sim'"))
    interface = Column(String(128), index=True)
    login_atend = Column(String(63), index=True, server_default=text("'full_users'"))
    cidade_ibge = Column(String(16))
    estado_ibge = Column(String(8))
    data_desbloq = Column(DateTime, server_default=text("'2015-01-01 00:00:00'"))
    pool_name = Column(String(30), server_default=text("'nenhum'"))
    rec_email = Column(Enum('sim', 'nao'), index=True, server_default=text("'sim'"))
    termo = Column(String(16))
    opcelular2 = Column(String(32), server_default=text("'nenhuma'"))
    dot_ref = Column(String(128), index=True)
    tipo_cliente = Column(Integer, server_default=text("'99'"))
    armario_olt = Column(String(96))
    conta_cartao = Column(Integer, server_default=text("'0'"))
    plano_bloqc = Column(String(64), index=True, server_default=text("'nenhum'"))
    uuid_cliente = Column(String(48), index=True)


class SisComprovante(Base):
    __tablename__ = 'sis_comprovante'

    id = Column(Integer, primary_key=True)
    login = Column(String(50), index=True)
    arquivo = Column(String(255))
    data = Column(DateTime)
    msg = Column(Text)
    titulo = Column(Integer)


t_sis_conectados = Table(
    'sis_conectados', metadata,
    Column('acctsessionid', String(32)),
    Column('login', String(64), nullable=False, index=True)
)


class SisConsulta(Base):
    __tablename__ = 'sis_consultas'

    id = Column(Integer, primary_key=True)
    cod = Column(String(32), nullable=False, index=True)
    query = Column(Text, nullable=False)


class SisContaspagar(Base):
    __tablename__ = 'sis_contaspagar'

    id = Column(Integer, primary_key=True)
    fornecedor = Column(String(255), index=True)
    vencimento = Column(DateTime)
    valor = Column(Numeric(12, 2))
    valorpago = Column(Numeric(12, 2), server_default=text("'0.00'"))
    emissao = Column(DateTime)
    nrdocumento = Column(String(50), index=True)
    usergerou = Column(String(50))
    historico = Column(String(255))
    planodecontas = Column(String(255))
    numparcelas = Column(Integer)
    observacao = Column(Text)
    parcatual = Column(Integer, server_default=text("'1'"))
    status = Column(String(50), index=True, server_default=text("'aberto'"))
    datapg = Column(DateTime)
    tipodiv = Column(Enum('for', 'fun'), server_default=text("'for'"))


class SisContato(Base):
    __tablename__ = 'sis_contato'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    login = Column(String(255), index=True)
    telefone = Column(String(255))
    assunto = Column(String(255))
    msg = Column(String)
    data = Column(DateTime)
    ip = Column(String(20))
    email = Column(String(255))
    arquivo = Column(String(255))


class SisContrato(Base):
    __tablename__ = 'sis_contrato'

    id = Column(Integer, primary_key=True)
    codigo = Column(String(8), index=True, server_default=text("'12345678'"))
    texto = Column(String)
    data = Column(DateTime)
    ativo = Column(String(3), server_default=text("'sim'"))
    nome = Column(String(255))
    padrao = Column(Enum('sim', 'nao'), nullable=False, server_default=text("'nao'"))


class SisDocumento(Base):
    __tablename__ = 'sis_documentos'

    id = Column(Integer, primary_key=True)
    codigo = Column(String(8), index=True)
    texto = Column(String)
    data = Column(DateTime)
    ativo = Column(String(3), server_default=text("'sim'"))
    nome = Column(String(255))
    tipo = Column(String(32), server_default=text("'clientes'"))


class SisDownload(Base):
    __tablename__ = 'sis_download'

    id = Column(Integer, primary_key=True)
    arquivo = Column(String(255))
    nome = Column(String(100), index=True)
    descricao = Column(String(255))
    cadastro = Column(DateTime)
    hit = Column(Integer)
    tipo = Column(String(5), server_default=text("'file'"))
    url = Column(String(255), index=True)
    categoria = Column(String(255), server_default=text("'geral'"))


t_sis_email = Table(
    'sis_email', metadata,
    Column('assuntoemail', String(255)),
    Column('msgemail', String),
    Column('assuntoemail5', String(255)),
    Column('msgemail5', String),
    Column('assuntoemail10', String(255)),
    Column('msgemail10', String),
    Column('assuntoemail15', String(255)),
    Column('msgemail15', String),
    Column('assuntoemailantes', String(255)),
    Column('msgemailantes', String),
    Column('assuntoemailaniv', String(255)),
    Column('msgemailaniv', String),
    Column('pdf', Enum('sim', 'nao'), server_default=text("'sim'")),
    Column('assuntoemail10antes', String(255)),
    Column('msgemail10antes', String),
    Column('msgsms', String(255)),
    Column('msgsms5', String(255)),
    Column('msgsms10', String(255)),
    Column('msgsms15', String(255)),
    Column('msgsmsantes', String(255)),
    Column('msgsms10antes', String(255)),
    Column('msgsmsaniv', String(255)),
    Column('msgsmscorte', String(255), server_default=text("'acesso bloqueado'")),
    Column('assuntomanual', String(255)),
    Column('msgmanual', String),
    Column('assuntoemaildesbloq', String(255)),
    Column('msgemaildesbloq', String),
    Column('pdf5', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('pdf10', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('pdf15', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('pdf5antes', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('pdf10antes', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('pdfmanual', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('msgsmsdesbloq', String(255)),
    Column('pdfcarne', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('assuntocarne', String(255)),
    Column('msgcarne', String),
    Column('assuntorecibo', String(255)),
    Column('msgrecibo', String),
    Column('assuntochamado', String(255), server_default=text("'chamado respondido'")),
    Column('msgchamado', String),
    Column('msgsmschamado', String(255), server_default=text("'chamado respondido'")),
    Column('assuntonfe', String(255)),
    Column('msgnfe', String),
    Column('msgsms_ondown', String(255), server_default=text("'limite de trafego atingido'"))
)


class SisEnviada(Base):
    __tablename__ = 'sis_enviadas'

    id = Column(Integer, primary_key=True)
    login = Column(String(255), nullable=False, index=True)
    data = Column(DateTime, nullable=False)
    tipo = Column(Enum('sms', 'web', 'app'), server_default=text("'web'"))
    mensagem = Column(String, nullable=False)
    uuid = Column(String(50), index=True)


class SisEstoque(Base):
    __tablename__ = 'sis_estoque'

    id = Column(Integer, primary_key=True)
    idprod = Column(Integer, nullable=False)
    qtdmin = Column(Integer, nullable=False)
    estoque = Column(Integer, nullable=False)


class SisFornecedor(Base):
    __tablename__ = 'sis_fornecedor'

    id = Column(Integer, primary_key=True)
    razaosoc = Column(String(255), index=True)
    nomefan = Column(String(255), index=True)
    contato = Column(String(255), index=True)
    endereco = Column(String(255))
    numero = Column(String(50))
    bairro = Column(String(255))
    cidade = Column(String(255))
    estado = Column(String(255))
    complemento = Column(String(255))
    telefone = Column(String(50))
    celular = Column(String(50))
    nextel = Column(String(50))
    fax = Column(String(50))
    email = Column(String(100), index=True)
    cpf_cnpj = Column(String(30), index=True)
    rg_ie = Column(String(30), index=True)
    tipo = Column(Enum('fisica', 'juridica'))
    cep = Column(String(11))
    obs = Column(Text)


class SisFunc(Base):
    __tablename__ = 'sis_func'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), index=True)
    sexo = Column(Enum('m', 'f'))
    nascimento = Column(String(20))
    telefone = Column(String(20))
    celular = Column(String(20))
    nextel = Column(String(20))
    cpf = Column(String(20))
    rg = Column(String(20))
    email = Column(String(50))
    cep = Column(String(11))
    endereco = Column(String(255))
    numero = Column(String(20))
    complemento = Column(String(255))
    estado = Column(String(2))
    cidade = Column(String(255))
    data_adm = Column(String(11))
    salario = Column(Numeric(12, 2))
    cargo = Column(String(50))
    comissao = Column(Numeric(12, 2))
    bairro = Column(String(255))
    tipo = Column(Enum('i', 't'), server_default=text("'i'"))


t_sis_hotsite = Table(
    'sis_hotsite', metadata,
    Column('fundo', String(10)),
    Column('pg_empresa', Text),
    Column('pg_tecnologia', Text),
    Column('pg_cobertura', Text),
    Column('pg_faq', Text),
    Column('pg_suporte', Text),
    Column('google', Text),
    Column('twitter', String(255), server_default=text("'pedrovigia'")),
    Column('tipotopo', String(3), server_default=text("'img'")),
    Column('arqtopo', String(255), server_default=text("'topo.jpg'")),
    Column('pg_confirmacao', Text),
    Column('anuncios', Text),
    Column('layout', String(255), server_default=text("'padrao'")),
    Column('preco', String(3), server_default=text("'sim'")),
    Column('anatel', String(3), server_default=text("'sim'")),
    Column('captcha', String(3), server_default=text("'sim'")),
    Column('batepapo', Enum('sim', 'nao'), server_default=text("'sim'"))
)


class SisIlanc(Base):
    __tablename__ = 'sis_ilanc'

    inum = Column(Integer, primary_key=True)
    ititulo = Column(Integer)
    inosso_num = Column(String(96))
    ilinha_dig = Column(String(255))
    icodigo_barras = Column(String(96))
    inum_conta = Column(Integer)
    irem_valor = Column(Numeric(12, 2))
    iperc_multa = Column(Numeric(12, 2))
    ivalor_multa = Column(Numeric(12, 2))
    iperc_mora = Column(Numeric(12, 2))
    ivalor_mora = Column(Numeric(12, 2))
    iperc_desc = Column(Numeric(12, 2))
    ivalor_desc = Column(Numeric(12, 2))
    inst1 = Column(String(255))
    inst2 = Column(String(255))
    token = Column(String(24), index=True)


class SisLanc(Base, handlers.BaseHandler):
    __tablename__ = 'sis_lanc'

    id = Column(Integer, primary_key=True)
    datavenc = Column(DateTime, index=True)
    nossonum = Column(String(64), index=True)
    datapag = Column(DateTime)
    nome = Column(String(255), index=True)
    recibo = Column(String(255), unique=True)
    status = Column(String(255), index=True, server_default=text("'aberto'"))
    login = Column(String(255), index=True)
    tipo = Column(String(255))
    obs = Column(String(255))
    processamento = Column(DateTime)
    aviso = Column(String(3), server_default=text("'nao'"))
    url = Column(String)
    usergerou = Column(String(20), index=True)
    valorger = Column(String(20), server_default=text("'completo'"))
    coletor = Column(String(20))
    linhadig = Column(String(255))
    valor = Column(String(50))
    valorpag = Column(String(50))
    gwt_numero = Column(String(32))
    imp = Column(Enum('sim', 'nao'), nullable=False, server_default=text("'nao'"))
    referencia = Column(String(8))
    tipocob = Column(Enum('fat', 'car'), nullable=False, server_default=text("'fat'"))
    codigo_carne = Column(String(32), index=True)
    chave_gnet = Column(String(32))
    numconta = Column(Integer)
    gerourem = Column(Enum('sim', 'nao'), server_default=text("'nao'"))
    remvalor = Column(Numeric(12, 2), index=True, server_default=text("'0.00'"))
    codigo_barras = Column(String(80))
    formapag = Column(String(100))
    fcartaobandeira = Column(String(100))
    fcartaonumero = Column(String(32))
    fchequenumero = Column(String(100))
    fchequebanco = Column(String(100))
    fchequeagcc = Column(String(100))
    percmulta = Column(Numeric(4, 2), server_default=text("'0.00'"))
    valormulta = Column(Numeric(12, 2), server_default=text("'0.00'"))
    percmora = Column(Numeric(4, 2), server_default=text("'0.00'"))
    valormora = Column(Numeric(12, 2), server_default=text("'0.00'"))
    percdesc = Column(Numeric(4, 2), server_default=text("'0.00'"))
    valordesc = Column(Numeric(12, 2), server_default=text("'0.00'"))
    deltitulo = Column(Integer, index=True, server_default=text("'0'"))
    num_recibos = Column(Integer, server_default=text("'0'"))
    num_retornos = Column(Integer, server_default=text("'0'"))
    alt_venc = Column(Integer, index=True, server_default=text("'0'"))
    uuid_lanc = Column(String(48), index=True)
    tarifa_paga = Column(Numeric(12, 2), server_default=text("'0.00'"))
    id_empresa = Column(String(16), unique=True)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_sa_instance_state']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def flatten(self, obj, data):
        data['contents'] = obj.contents
        return data

# handlers.register(SisLanc, handlers.BaseHandler)


class SisLink(Base):
    __tablename__ = 'sis_links'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    endereco = Column(String(255))
    hits = Column(Integer)
    destino = Column(String(50))


class SisLog(Base):
    __tablename__ = 'sis_logs'

    registro = Column(String)
    data = Column(String(255))
    login = Column(String(64))
    tipo = Column(String(20), server_default=text("'admin'"))
    operacao = Column(String(8), server_default=text("'OPERNULL'"))
    id = Column(Integer, primary_key=True)


class SisMlanc(Base):
    __tablename__ = 'sis_mlanc'

    id = Column(Integer, primary_key=True)
    idlanc = Column(Integer, index=True)
    valor = Column(Numeric(12, 2))
    tipo = Column(String(50))
    desc = Column(String(255))
    deltitulo = Column(Integer, index=True, server_default=text("'0'"))


class SisMsg(Base):
    __tablename__ = 'sis_msg'

    id = Column(Integer, primary_key=True)
    chamado = Column(String(255))
    msg = Column(Text)
    tipo = Column(String(10), nullable=False, server_default=text("'F5F5F5'"))
    login = Column(String(255), index=True)
    atendente = Column(String(255))
    msg_data = Column(DateTime)


class SisNewsletter(Base):
    __tablename__ = 'sis_newsletter'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    email = Column(String(255))


class SisNfe(Base):
    __tablename__ = 'sis_nfe'

    id = Column(Integer, primary_key=True)
    modelo = Column(String(32), nullable=False)
    numero = Column(Integer, nullable=False)
    serie = Column(String(8), nullable=False)
    referencia = Column(String(8), nullable=False)
    emissao = Column(DateTime, nullable=False)
    cfop = Column(String(4), nullable=False)
    login = Column(String(64), nullable=False)
    id_titulo = Column(Integer, nullable=False, index=True)
    base_calculo = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    aliquota = Column(Numeric(4, 2), nullable=False, server_default=text("'0.00'"))
    valor_icms = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    isentas = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    outros = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    valor_total = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    chave = Column(String(32), nullable=False, index=True)
    arquivo = Column(String(36), nullable=False)
    obs = Column(String(255))
    perc_ibpt = Column(Numeric(4, 2), server_default=text("'0.00'"))
    perc_ibpt_m = Column(Numeric(4, 2), server_default=text("'0.00'"))
    perc_ibpt_e = Column(Numeric(4, 2), server_default=text("'0.00'"))
    perc_ibpt_f = Column(Numeric(4, 2), server_default=text("'0.00'"))
    regime = Column(Enum('simples', 'lucro'))
    situacao = Column(Enum('S', 'R', 'C', 'N'), server_default=text("'N'"))
    info_del = Column(String(32))
    pis = Column(Numeric(12, 2), server_default=text("'0.00'"))
    valor_pis = Column(Numeric(12, 2), server_default=text("'0.00'"))
    cofins = Column(Numeric(12, 2), server_default=text("'0.00'"))
    valor_cofins = Column(Numeric(12, 2), server_default=text("'0.00'"))
    tipo = Column(Integer, server_default=text("'4'"))


t_sis_nfeitens = Table(
    'sis_nfeitens', metadata,
    Column('chave_item', String(32), nullable=False, index=True),
    Column('desc_item', String(40), nullable=False),
    Column('icms_item', Numeric(9, 2), nullable=False, server_default=text("'0.00'")),
    Column('aliq_item', Numeric(4, 2), nullable=False, server_default=text("'0.00'")),
    Column('outros_item', Numeric(10, 2), nullable=False, server_default=text("'0.00'")),
    Column('valor_item', Numeric(9, 2), nullable=False, server_default=text("'0.00'")),
    Column('cod_item', String(4), nullable=False, server_default=text("'0104'")),
    Column('megas', String(16)),
    Column('pis_item', Numeric(12, 2), server_default=text("'0.00'")),
    Column('valor_itempis', Numeric(12, 2), server_default=text("'0.00'")),
    Column('cofins_item', Numeric(12, 2), server_default=text("'0.00'")),
    Column('valor_itemcofins', Numeric(12, 2), server_default=text("'0.00'"))
)


class SisNota(Base):
    __tablename__ = 'sis_notas'

    id = Column(Integer, primary_key=True)
    texto = Column(String)
    data = Column(DateTime)
    token = Column(String(32), index=True)
    usuario = Column(String(50))


class SisNoticia(Base):
    __tablename__ = 'sis_noticia'

    id = Column(Integer, primary_key=True)
    titulo = Column(String(255))
    noticia = Column(Text)
    data = Column(DateTime)
    autor = Column(String(255))
    hit = Column(Integer, server_default=text("'1'"))


class SisNotificaco(Base):
    __tablename__ = 'sis_notificacoes'

    id = Column(Integer, primary_key=True)
    data = Column(DateTime, nullable=False)
    dados = Column(Text, nullable=False)
    servico = Column(String(32), nullable=False)


class SisOpcao(Base):
    __tablename__ = 'sis_opcao'

    id = Column(Integer, primary_key=True)
    nome = Column(String(64), unique=True)
    valor = Column(String(255))


class SisPagina(Base):
    __tablename__ = 'sis_paginas'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    conteudo = Column(String)
    cadastro = Column(DateTime)


class SisPerm(Base):
    __tablename__ = 'sis_perm'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    usuario = Column(String(50))
    data = Column(DateTime)
    permissao = Column(Enum('sim', 'nao'), server_default=text("'sim'"))


class SisPlano(Base):
    __tablename__ = 'sis_plano'

    nome = Column(String(255), primary_key=True)
    valor = Column(String(255), nullable=False, index=True)
    velup = Column(String(50))
    veldown = Column(String(50))
    garup = Column(String(50))
    gardown = Column(String(50))
    tempoup = Column(String(50))
    tempodown = Column(String(50))
    prioridade = Column(String(50))
    maxup = Column(String(50))
    maxdown = Column(String(50))
    desaup = Column(String(50))
    desadown = Column(String(50))
    burst = Column(String(50))
    descricao = Column(Text)
    oculto = Column(String(3), server_default=text("'nao'"))
    valor_scm = Column(Numeric(12, 2), server_default=text("'0.00'"))
    valor_sva = Column(Numeric(12, 2), server_default=text("'0.00'"))
    pool = Column(String(50))
    valor_desc = Column(Numeric(12, 2), server_default=text("'0.00'"))
    list = Column(String(50))
    aliquota = Column(Numeric(12, 2), server_default=text("'19.25'"))
    cfop_plano = Column(String(8))
    desc_titulo = Column(String(255))
    perc_ibpt = Column(Numeric(4, 2), server_default=text("'0.00'"))
    tipo = Column(String(31), server_default=text("'semi-dedicado'"))
    ipv6a = Column(String(128))
    ipv6b = Column(String(128))
    vpm = Column(Numeric(12, 2), server_default=text("'0.00'"))
    faixa = Column(Integer, server_default=text("'99'"))
    tecnologia = Column(String(8), server_default=text("'I'"))
    pis_pasep = Column(Numeric(12, 2), server_default=text("'0.00'"))
    cofins = Column(Numeric(12, 2), server_default=text("'0.00'"))
    perc_ibpt_m = Column(Numeric(4, 2), server_default=text("'0.00'"))
    perc_ibpt_e = Column(Numeric(4, 2), server_default=text("'0.00'"))
    perc_ibpt_f = Column(Numeric(4, 2), server_default=text("'0.00'"))


class SisPool(Base):
    __tablename__ = 'sis_pool'

    id = Column(Integer, primary_key=True)
    nome = Column(String(32), nullable=False, unique=True)
    chave = Column(String(40), index=True)
    ip_inicial = Column(String(255), nullable=False)
    ip_final = Column(String(255), nullable=False)
    data_uso = Column(DateTime)
    total_ips = Column(Integer)
    usuario = Column(String(64), nullable=False)


class SisProdcliente(Base):
    __tablename__ = 'sis_prodcliente'

    id = Column(Integer, primary_key=True)
    idprod = Column(Integer, nullable=False)
    qtdcli = Column(Integer, nullable=False)
    datains = Column(DateTime, nullable=False)
    usuario = Column(String(32), nullable=False)
    cliente = Column(String(32), nullable=False, index=True)


class SisProdhistorico(Base):
    __tablename__ = 'sis_prodhistorico'

    id = Column(Integer, primary_key=True)
    idprod = Column(Integer, nullable=False, index=True)
    usuario = Column(String(32), nullable=False)
    historico = Column(String(255), nullable=False)
    data = Column(DateTime, nullable=False)


class SisProduto(Base):
    __tablename__ = 'sis_produto'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False, unique=True)
    idforn = Column(Integer, nullable=False)
    descricao = Column(String)
    precoatual = Column(Numeric(12, 2), nullable=False)
    precovelho = Column(Numeric(12, 2))
    precocusto = Column(Numeric(12, 2))
    datacad = Column(DateTime, nullable=False)
    ultcompra = Column(DateTime)
    ultalteracao = Column(Numeric(10, 0))
    peso = Column(Numeric(12, 2))
    ativo = Column(Enum('sim', 'nao'), nullable=False)
    codbarras = Column(String(255))
    grupo = Column(String(128))
    med = Column(String(3))
    aplicacao = Column(String)
    ipi = Column(Integer)
    icms = Column(Integer)
    codigo = Column(String(50))


class SisProvedor(Base):
    __tablename__ = 'sis_provedor'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    endereco = Column(String(255), nullable=False)
    bairro = Column(String(255), nullable=False)
    cidade = Column(String(255), nullable=False)
    estado = Column(String(255), nullable=False)
    fone = Column(String(255), nullable=False)
    site = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    cep = Column(String(255), nullable=False)
    cnpj = Column(String(255), nullable=False)
    responsavel = Column(String(255), nullable=False)
    token = Column(String(5), server_default=text("'12345'"))
    celular = Column(String(255))
    razao = Column(String(255))
    fax = Column(String(50))
    nextel = Column(String(50))
    zero_oito = Column(String(31))
    ie = Column(String(32), server_default=text("'isento'"))
    cargo = Column(String(64), server_default=text("'gerente'"))
    fistel = Column(String(32))
    coordenadas = Column(String(64), server_default=text("'-10.00,-50.00'"))


class SisRemessa(Base):
    __tablename__ = 'sis_remessa'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    conta = Column(Integer, index=True)
    md5sum = Column(String(32))
    dataproc = Column(DateTime)
    usuario = Column(String(255))
    token = Column(String(8), index=True)
    cnab = Column(String(3), index=True)
    dataenv = Column(DateTime)
    nomearq = Column(String(50))


class SisResumo(Base):
    __tablename__ = 'sis_resumo'

    id = Column(Integer, primary_key=True)
    dados = Column(String(20), server_default=text("'x'"))
    tempo = Column(String(20), server_default=text("'x'"))
    conexoes = Column(String(20), server_default=text("'x'"))
    chamados = Column(String(20), server_default=text("'x'"))
    contas = Column(String(20), server_default=text("'x'"))
    mes = Column(String(2), server_default=text("'x'"))
    ano = Column(String(4), server_default=text("'x'"))
    resumo = Column(String(6), server_default=text("'032011'"))
    login = Column(String(50), index=True)
    data = Column(DateTime)


class SisRetorno(Base):
    __tablename__ = 'sis_retorno'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    conta = Column(Integer, index=True)
    md5sum = Column(String(32))
    dataarq = Column(DateTime)
    dataproc = Column(DateTime)
    usuario = Column(String(255))
    token = Column(String(8), index=True)
    cnab = Column(String(3), index=True)


class SisSercontrato(Base):
    __tablename__ = 'sis_sercontratos'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    valor = Column(Numeric(12, 2), nullable=False, server_default=text("'0.00'"))
    incluir = Column(Enum('sim', 'nao'), nullable=False, server_default=text("'sim'"))
    data = Column(DateTime, nullable=False)
    insuser = Column(String(50), nullable=False)
    login = Column(String(100), nullable=False)


class SisSici(Base):
    __tablename__ = 'sis_sici'

    id = Column(Integer, primary_key=True)
    referencia = Column(String(16))
    arquivo = Column(String(64))
    data = Column(DateTime)
    user_gerou = Column(String(64))


class SisSolic(Base):
    __tablename__ = 'sis_solic'

    id = Column(Integer, primary_key=True)
    login = Column(String(64), index=True)
    senha = Column(String(32))
    email = Column(String(255))
    nome = Column(String(255))
    data_nasc = Column(String(20))
    cpf = Column(String(20), index=True)
    endereco = Column(String(255))
    bairro = Column(String(255))
    cidade = Column(String(255))
    estado = Column(String(10))
    cep = Column(String(20))
    telefone = Column(String(255))
    vencimento = Column(String(255))
    plano = Column(String(255))
    complemento = Column(String(255))
    rg = Column(String(255))
    celular = Column(String(50))
    comodato = Column(String(3), server_default=text("'nao'"))
    datainst = Column(String(100))
    visitado = Column(String(3), server_default=text("'nao'"))
    instalado = Column(String(3), server_default=text("'nao'"))
    tecnico = Column(String(255), index=True)
    obs = Column(Text)
    tipo = Column(String(20), server_default=text("'assinatura'"))
    ip = Column(String(20))
    mac = Column(String(17))
    valor = Column(String(50))
    concluido = Column(String(3), server_default=text("'nao'"))
    promocod = Column(String(50), server_default=text("'nao'"))
    numero = Column(String(20))
    endereco_res = Column(String(255))
    numero_res = Column(String(20))
    bairro_res = Column(String(255))
    cidade_res = Column(String(255))
    cep_res = Column(String(9))
    estado_res = Column(String(2))
    complemento_res = Column(String(255))
    vendedor = Column(String(255))
    nextel = Column(String(50))
    disp = Column(Enum('sim', 'nao'), nullable=False, server_default=text("'sim'"))
    contrato = Column(String(8), server_default=text("'nenhum'"))
    adesao = Column(Numeric(12, 2), server_default=text("'0.00'"))
    visita = Column(DateTime)
    equipamento = Column(String(20), server_default=text("'nenhum'"))
    codigo = Column(String(255))
    ipcadastro = Column(String(150))
    processamento = Column(DateTime)
    opcelular = Column(String(100), server_default=text("'nenhuma'"))
    status = Column(Enum('aberto', 'concluido', 'pendente', 'atrasado'), server_default=text("'aberto'"))
    coordenadas = Column(String(127))
    login_atend = Column(String(63), index=True, server_default=text("'full_users'"))
    ramal = Column(String(255))
    termo = Column(String(16))
    opcelular2 = Column(String(32), server_default=text("'nenhuma'"))
    celular2 = Column(String(32))
    naturalidade = Column(String(50))
    dot_ref = Column(String(128))


class SisSuporte(Base):
    __tablename__ = 'sis_suporte'

    id = Column(Integer, primary_key=True)
    assunto = Column(String(255))
    abertura = Column(DateTime)
    fechamento = Column(DateTime)
    email = Column(String(255))
    status = Column(String(255), server_default=text("'aberto'"))
    chamado = Column(String(255), index=True)
    nome = Column(String(255))
    login = Column(String(255), index=True)
    atendente = Column(String(255))
    visita = Column(DateTime, index=True)
    prioridade = Column(String(20), server_default=text("'normal'"))
    ramal = Column(String(20), server_default=text("'todos'"))
    reply = Column(Enum('sim', 'nao'), server_default=text("'nao'"))
    tecnico = Column(Integer)
    login_atend = Column(String(63), index=True, server_default=text("'full_users'"))
    motivo_fechar = Column(String)


class TabGnet(Base):
    __tablename__ = 'tab_gnet'

    id = Column(Integer, primary_key=True)
    transacao = Column(String(64), nullable=False)
    titulo = Column(Integer, nullable=False)
    data = Column(DateTime)
    status = Column(String(16), server_default=text("'new'"))


class TabPlaca(Base):
    __tablename__ = 'tab_placa'

    id = Column(Integer, primary_key=True)
    placa = Column(String(10), server_default=text("'eth0'"))
    ip = Column(String(255), nullable=False, unique=True, server_default=text("''"))
    mascara = Column(String(255))
    roteador = Column(String(255))


class TabSinal(Base):
    __tablename__ = 'tab_sinal'

    id = Column(Integer, primary_key=True)
    idapi = Column(String(10))
    sinal = Column(String(50))
    mac = Column(String(50), index=True)
    cartao = Column(String(50))
    rate = Column(String(50))
    data = Column(DateTime)


t_vtab_comerros = Table(
    'vtab_comerros', metadata,
    Column('tentativas', BigInteger, server_default=text("'0'")),
    Column('id', Integer, server_default=text("'0'")),
    Column('nome', String(255)),
    Column('email', String(255)),
    Column('endereco', String(255)),
    Column('bairro', String(255)),
    Column('cidade', String(255)),
    Column('cep', String(9)),
    Column('estado', String(2)),
    Column('cpf_cnpj', String(20)),
    Column('fone', String(50)),
    Column('obs', Text),
    Column('nascimento', String(255)),
    Column('cadastro', String(255)),
    Column('login', String(64)),
    Column('tipo', String(10)),
    Column('night', String(3), server_default=text("'nao'")),
    Column('aviso', Text),
    Column('foto', String(255)),
    Column('venc', String(2), server_default=text("'01'")),
    Column('mac', String(17)),
    Column('complemento', String(255)),
    Column('ip', String(20)),
    Column('ramal', String(255)),
    Column('rg', String(255)),
    Column('isento', String(3), server_default=text("'nao'")),
    Column('celular', String(50)),
    Column('bloqueado', String(3), server_default=text("'nao'")),
    Column('autoip', String(3), server_default=text("'sim'")),
    Column('automac', String(3), server_default=text("'sim'")),
    Column('conta', String(11), server_default=text("'1'")),
    Column('ipvsix', String(255)),
    Column('plano', String(255)),
    Column('send', String(3), server_default=text("'nao'")),
    Column('cli_ativado', Enum('s', 'n'), server_default=text("'s'")),
    Column('simultaneo', String(3), server_default=text("'nao'")),
    Column('turbo', String(255), server_default=text("'nenhum'")),
    Column('comodato', String(3), server_default=text("'nao'")),
    Column('observacao', String(3), server_default=text("'nao'")),
    Column('chavetipo', String(10)),
    Column('chave', String(255)),
    Column('contrato', String(8), server_default=text("'87654321'")),
    Column('ssid', String(255)),
    Column('senha', String(255)),
    Column('numero', String(20)),
    Column('responsavel', String(255)),
    Column('nome_pai', String(255)),
    Column('nome_mae', String(255)),
    Column('expedicao_rg', String(20)),
    Column('naturalidade', String(50)),
    Column('acessacen', String(50), server_default=text("'sim'")),
    Column('pessoa', String(10), server_default=text("'fisica'")),
    Column('endereco_res', String(255)),
    Column('numero_res', String(20)),
    Column('bairro_res', String(255)),
    Column('cidade_res', String(255)),
    Column('cep_res', String(9)),
    Column('estado_res', String(2)),
    Column('complemento_res', String(255)),
    Column('desconto', Numeric(12, 2), server_default=text("'0.00'")),
    Column('acrescimo', Numeric(12, 2), server_default=text("'0.00'")),
    Column('equipamento', String(20), server_default=text("'nenhum'")),
    Column('vendedor', String(255)),
    Column('nextel', String(50)),
    Column('accesslist', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('resumo', String(6), server_default=text("'032011'")),
    Column('grupo', String(50)),
    Column('codigo', String(50)),
    Column('prilanc', Enum('pro', 'tot'), server_default=text("'pro'")),
    Column('tipobloq', Enum('aut', 'man'), server_default=text("'aut'")),
    Column('adesao', Numeric(12, 2), server_default=text("'0.00'")),
    Column('mbdisco', Integer, server_default=text("'100'")),
    Column('impsel', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('sms', Enum('sim', 'nao'), server_default=text("'sim'")),
    Column('ltrafego', BigInteger, server_default=text("'0'")),
    Column('planodown', String(255), server_default=text("'nenhum'")),
    Column('ligoudown', String(6), server_default=text("'012011'")),
    Column('statusdown', Enum('on', 'off'), server_default=text("'off'")),
    Column('statusturbo', Enum('on', 'off'), server_default=text("'off'")),
    Column('opcelular', String(100), server_default=text("'nenhuma'")),
    Column('nome_res', String(255)),
    Column('coordenadas', String(64)),
    Column('rem_obs', DateTime),
    Column('valor_sva', Numeric(12, 2), server_default=text("'0.00'")),
    Column('dias_corte', Integer, server_default=text("'999'")),
    Column('user_ip', String(100)),
    Column('user_mac', String(100)),
    Column('data_ip', DateTime),
    Column('data_mac', DateTime),
    Column('last_update', DateTime),
    Column('data_bloq', DateTime),
    Column('tags', String),
    Column('tecnico', String(255)),
    Column('data_ins', DateTime),
    Column('altsenha', Enum('sim', 'nao')),
    Column('geranfe', Enum('sim', 'nao'), server_default=text("'sim'")),
    Column('mesref', Enum('now', 'ant'), server_default=text("'ant'")),
    Column('ipfall', String(32)),
    Column('tit_abertos', Integer),
    Column('parc_abertas', Integer),
    Column('tipo_pessoa', Integer),
    Column('celular2', String(32)),
    Column('mac_serial', String(255)),
    Column('status_corte', Enum('full', 'down', 'bloq'), server_default=text("'full'")),
    Column('plano15', String(255), server_default=text("'nenhum'")),
    Column('pgaviso', Enum('sim', 'nao'), server_default=text("'sim'")),
    Column('porta_olt', String(32)),
    Column('caixa_herm', String(128)),
    Column('porta_splitter', String(32)),
    Column('onu_ont', String(64)),
    Column('switch', String(128)),
    Column('tit_vencidos', Integer),
    Column('pgcorte', Enum('sim', 'nao'), server_default=text("'sim'")),
    Column('interface', String(128)),
    Column('login_atend', String(63), server_default=text("'full_users'")),
    Column('cidade_ibge', String(16)),
    Column('estado_ibge', String(8)),
    Column('data_desbloq', DateTime, server_default=text("'2015-01-01 00:00:00'")),
    Column('pool_name', String(30), server_default=text("'nenhum'")),
    Column('rec_email', Enum('sim', 'nao'), server_default=text("'sim'")),
    Column('termo', String(16)),
    Column('opcelular2', String(32), server_default=text("'nenhuma'")),
    Column('dot_ref', String(128)),
    Column('tipo_cliente', Integer, server_default=text("'99'")),
    Column('armario_olt', String(96)),
    Column('conta_cartao', Integer, server_default=text("'0'")),
    Column('plano_bloqc', String(64), server_default=text("'nenhum'")),
    Column('uuid_cliente', String(48))
)


t_vtab_desbloqueio = Table(
    'vtab_desbloqueio', metadata,
    Column('login', String(64)),
    Column('id', Integer, server_default=text("'0'")),
    Column('celular', String(50)),
    Column('nome_res', String(255)),
    Column('email', String(255)),
    Column('dias_corte', Integer, server_default=text("'999'")),
    Column('datavenc', DateTime),
    Column('titulo', Integer, server_default=text("'0'")),
    Column('deltitulo', Integer, server_default=text("'0'"))
)


t_vtab_gnetrem = Table(
    'vtab_gnetrem', metadata,
    Column('id', Integer, server_default=text("'0'")),
    Column('nome', String(255)),
    Column('email', String(255)),
    Column('endereco', String(255)),
    Column('bairro', String(255)),
    Column('cidade', String(255)),
    Column('cep', String(9)),
    Column('estado', String(2)),
    Column('cpf_cnpj', String(20)),
    Column('fone', String(50)),
    Column('obs', Text),
    Column('nascimento', String(255)),
    Column('cadastro', String(255)),
    Column('login', String(64)),
    Column('tipo', String(10)),
    Column('night', String(3), server_default=text("'nao'")),
    Column('aviso', Text),
    Column('foto', String(255)),
    Column('venc', String(2), server_default=text("'01'")),
    Column('mac', String(17)),
    Column('complemento', String(255)),
    Column('ip', String(20)),
    Column('ramal', String(255)),
    Column('rg', String(255)),
    Column('isento', String(3), server_default=text("'nao'")),
    Column('celular', String(50)),
    Column('bloqueado', String(3), server_default=text("'nao'")),
    Column('autoip', String(3), server_default=text("'sim'")),
    Column('automac', String(3), server_default=text("'sim'")),
    Column('conta', String(11), server_default=text("'1'")),
    Column('ipvsix', String(255)),
    Column('plano', String(255)),
    Column('send', String(3), server_default=text("'nao'")),
    Column('cli_ativado', Enum('s', 'n'), server_default=text("'s'")),
    Column('simultaneo', String(3), server_default=text("'nao'")),
    Column('turbo', String(255), server_default=text("'nenhum'")),
    Column('comodato', String(3), server_default=text("'nao'")),
    Column('observacao', String(3), server_default=text("'nao'")),
    Column('chavetipo', String(10)),
    Column('chave', String(255)),
    Column('contrato', String(8), server_default=text("'87654321'")),
    Column('ssid', String(255)),
    Column('senha', String(255)),
    Column('numero', String(20)),
    Column('responsavel', String(255)),
    Column('nome_pai', String(255)),
    Column('nome_mae', String(255)),
    Column('expedicao_rg', String(20)),
    Column('naturalidade', String(50)),
    Column('acessacen', String(50), server_default=text("'sim'")),
    Column('pessoa', String(10), server_default=text("'fisica'")),
    Column('endereco_res', String(255)),
    Column('numero_res', String(20)),
    Column('bairro_res', String(255)),
    Column('cidade_res', String(255)),
    Column('cep_res', String(9)),
    Column('estado_res', String(2)),
    Column('complemento_res', String(255)),
    Column('desconto', Numeric(12, 2), server_default=text("'0.00'")),
    Column('acrescimo', Numeric(12, 2), server_default=text("'0.00'")),
    Column('equipamento', String(20), server_default=text("'nenhum'")),
    Column('vendedor', String(255)),
    Column('nextel', String(50)),
    Column('accesslist', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('resumo', String(6), server_default=text("'032011'")),
    Column('grupo', String(50)),
    Column('codigo', String(50)),
    Column('prilanc', Enum('pro', 'tot'), server_default=text("'pro'")),
    Column('tipobloq', Enum('aut', 'man'), server_default=text("'aut'")),
    Column('adesao', Numeric(12, 2), server_default=text("'0.00'")),
    Column('mbdisco', Integer, server_default=text("'100'")),
    Column('impsel', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('sms', Enum('sim', 'nao'), server_default=text("'sim'")),
    Column('ltrafego', BigInteger, server_default=text("'0'")),
    Column('planodown', String(255), server_default=text("'nenhum'")),
    Column('ligoudown', String(6), server_default=text("'012011'")),
    Column('statusdown', Enum('on', 'off'), server_default=text("'off'")),
    Column('statusturbo', Enum('on', 'off'), server_default=text("'off'")),
    Column('opcelular', String(100), server_default=text("'nenhuma'")),
    Column('nome_res', String(255)),
    Column('coordenadas', String(64)),
    Column('rem_obs', DateTime),
    Column('valor_sva', Numeric(12, 2), server_default=text("'0.00'")),
    Column('dias_corte', Integer, server_default=text("'999'")),
    Column('user_ip', String(100)),
    Column('user_mac', String(100)),
    Column('data_ip', DateTime),
    Column('data_mac', DateTime),
    Column('last_update', DateTime),
    Column('data_bloq', DateTime),
    Column('tags', String),
    Column('tecnico', String(255)),
    Column('data_ins', DateTime),
    Column('altsenha', Enum('sim', 'nao')),
    Column('geranfe', Enum('sim', 'nao'), server_default=text("'sim'")),
    Column('mesref', Enum('now', 'ant'), server_default=text("'ant'")),
    Column('ipfall', String(32)),
    Column('tit_abertos', Integer),
    Column('parc_abertas', Integer),
    Column('tipo_pessoa', Integer),
    Column('celular2', String(32)),
    Column('mac_serial', String(255)),
    Column('status_corte', Enum('full', 'down', 'bloq'), server_default=text("'full'")),
    Column('plano15', String(255), server_default=text("'nenhum'")),
    Column('pgaviso', Enum('sim', 'nao'), server_default=text("'sim'")),
    Column('porta_olt', String(32)),
    Column('caixa_herm', String(128)),
    Column('porta_splitter', String(32)),
    Column('onu_ont', String(64)),
    Column('switch', String(128)),
    Column('tit_vencidos', Integer),
    Column('pgcorte', Enum('sim', 'nao'), server_default=text("'sim'")),
    Column('interface', String(128)),
    Column('login_atend', String(63), server_default=text("'full_users'")),
    Column('cidade_ibge', String(16)),
    Column('estado_ibge', String(8)),
    Column('data_desbloq', DateTime, server_default=text("'2015-01-01 00:00:00'")),
    Column('pool_name', String(30), server_default=text("'nenhum'")),
    Column('rec_email', Enum('sim', 'nao'), server_default=text("'sim'")),
    Column('termo', String(16)),
    Column('opcelular2', String(32), server_default=text("'nenhuma'")),
    Column('dot_ref', String(128)),
    Column('tipo_cliente', Integer, server_default=text("'99'")),
    Column('armario_olt', String(96)),
    Column('conta_cartao', Integer, server_default=text("'0'")),
    Column('plano_bloqc', String(64), server_default=text("'nenhum'")),
    Column('uuid_cliente', String(48)),
    Column('descricao', String(255)),
    Column('tipolanc', String(255)),
    Column('valorlanc', String(50)),
    Column('idlanc', Integer, server_default=text("'0'")),
    Column('datavenclanc', DateTime),
    Column('deltitulo', Integer, server_default=text("'0'"))
)


t_vtab_mtitulos = Table(
    'vtab_mtitulos', metadata,
    Column('id', Integer, server_default=text("'0'")),
    Column('idlanc', Integer),
    Column('valor', Numeric(12, 2)),
    Column('tipo', String(50)),
    Column('desc', String(255)),
    Column('deltitulo', Integer, server_default=text("'0'")),
    Column('datavenc', DateTime),
    Column('datapag', DateTime),
    Column('status', String(255), server_default=text("'aberto'")),
    Column('login', String(255)),
    Column('bloqueado', String(3), server_default=text("'nao'")),
    Column('mesref', Enum('now', 'ant'), server_default=text("'ant'")),
    Column('cli_ativado', Enum('s', 'n'), server_default=text("'s'"))
)


t_vtab_newtitulo = Table(
    'vtab_newtitulo', metadata,
    Column('id', Integer, server_default=text("'0'")),
    Column('nome', String(255)),
    Column('isento', String(3), server_default=text("'nao'")),
    Column('venc', String(2), server_default=text("'01'")),
    Column('login', String(64)),
    Column('conta', String(11), server_default=text("'1'")),
    Column('plano', String(255)),
    Column('mesref', Enum('now', 'ant'), server_default=text("'ant'")),
    Column('desconto', Numeric(12, 2), server_default=text("'0.00'")),
    Column('acrescimo', Numeric(12, 2), server_default=text("'0.00'")),
    Column('email', String(255)),
    Column('prilanc', Enum('pro', 'tot'), server_default=text("'pro'")),
    Column('cpf_cnpj', String(20)),
    Column('cep_res', String(9)),
    Column('endereco_res', String(255)),
    Column('numero_res', String(20)),
    Column('bairro_res', String(255)),
    Column('complemento_res', String(255)),
    Column('estado_res', String(2)),
    Column('cidade_res', String(255)),
    Column('titulo', Integer, server_default=text("'0'")),
    Column('deltitulo', Integer, server_default=text("'0'"))
)


t_vtab_remtitulos01 = Table(
    'vtab_remtitulos01', metadata,
    Column('nome', String(255)),
    Column('email', String(255)),
    Column('endereco', String(255)),
    Column('complemento', String(255)),
    Column('bairro', String(255)),
    Column('cidade', String(255)),
    Column('cep', String(9)),
    Column('estado', String(2)),
    Column('cpf_cnpj', String(20)),
    Column('login', String(64)),
    Column('venc', String(2), server_default=text("'01'")),
    Column('numero', String(20)),
    Column('cli_ativado', Enum('s', 'n'), server_default=text("'s'")),
    Column('bloqueado', String(3), server_default=text("'nao'")),
    Column('mesref', Enum('now', 'ant'), server_default=text("'ant'")),
    Column('plano', String(255)),
    Column('grupo', String(50)),
    Column('ramal', String(255)),
    Column('valor', Numeric(12, 2), server_default=text("'0.00'")),
    Column('titulo', Integer, server_default=text("'0'")),
    Column('datavenc', DateTime),
    Column('referencia', String(8)),
    Column('nossonum', String(64)),
    Column('processamento', DateTime),
    Column('gerourem', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('percmulta', Numeric(4, 2), server_default=text("'0.00'")),
    Column('valormulta', Numeric(12, 2), server_default=text("'0.00'")),
    Column('percmora', Numeric(4, 2), server_default=text("'0.00'")),
    Column('valormora', Numeric(12, 2), server_default=text("'0.00'")),
    Column('percdesc', Numeric(4, 2), server_default=text("'0.00'")),
    Column('valordesc', Numeric(12, 2), server_default=text("'0.00'")),
    Column('deltitulo', Integer, server_default=text("'0'")),
    Column('numconta', Integer),
    Column('alt_venc', Integer, server_default=text("'0'")),
    Column('cod_ocorrencia', String(2))
)


t_vtab_remtitulos02 = Table(
    'vtab_remtitulos02', metadata,
    Column('nome', String(255)),
    Column('email', String(255)),
    Column('endereco', String(255)),
    Column('complemento', String(255)),
    Column('bairro', String(255)),
    Column('cidade', String(255)),
    Column('cep', String(9)),
    Column('estado', String(2)),
    Column('cpf_cnpj', String(20)),
    Column('login', String(64)),
    Column('venc', String(2), server_default=text("'01'")),
    Column('numero', String(20)),
    Column('cli_ativado', Enum('s', 'n'), server_default=text("'s'")),
    Column('bloqueado', String(3), server_default=text("'nao'")),
    Column('mesref', Enum('now', 'ant'), server_default=text("'ant'")),
    Column('plano', String(255)),
    Column('grupo', String(50)),
    Column('ramal', String(255)),
    Column('valor', Numeric(12, 2), server_default=text("'0.00'")),
    Column('titulo', Integer, server_default=text("'0'")),
    Column('datavenc', DateTime),
    Column('referencia', String(8)),
    Column('nossonum', String(64)),
    Column('processamento', DateTime),
    Column('gerourem', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('percmulta', Numeric(4, 2), server_default=text("'0.00'")),
    Column('valormulta', Numeric(12, 2), server_default=text("'0.00'")),
    Column('percmora', Numeric(4, 2), server_default=text("'0.00'")),
    Column('valormora', Numeric(12, 2), server_default=text("'0.00'")),
    Column('percdesc', Numeric(4, 2), server_default=text("'0.00'")),
    Column('valordesc', Numeric(12, 2), server_default=text("'0.00'")),
    Column('deltitulo', Integer, server_default=text("'0'")),
    Column('numconta', Integer),
    Column('alt_venc', Integer, server_default=text("'0'")),
    Column('cod_ocorrencia', String(2))
)


t_vtab_remtitulos06 = Table(
    'vtab_remtitulos06', metadata,
    Column('nome', String(255)),
    Column('email', String(255)),
    Column('endereco', String(255)),
    Column('complemento', String(255)),
    Column('bairro', String(255)),
    Column('cidade', String(255)),
    Column('cep', String(9)),
    Column('estado', String(2)),
    Column('cpf_cnpj', String(20)),
    Column('login', String(64)),
    Column('venc', String(2), server_default=text("'01'")),
    Column('numero', String(20)),
    Column('cli_ativado', Enum('s', 'n'), server_default=text("'s'")),
    Column('bloqueado', String(3), server_default=text("'nao'")),
    Column('mesref', Enum('now', 'ant'), server_default=text("'ant'")),
    Column('plano', String(255)),
    Column('grupo', String(50)),
    Column('ramal', String(255)),
    Column('valor', Numeric(12, 2), server_default=text("'0.00'")),
    Column('titulo', Integer, server_default=text("'0'")),
    Column('datavenc', DateTime),
    Column('referencia', String(8)),
    Column('nossonum', String(64)),
    Column('processamento', DateTime),
    Column('gerourem', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('percmulta', Numeric(4, 2), server_default=text("'0.00'")),
    Column('valormulta', Numeric(12, 2), server_default=text("'0.00'")),
    Column('percmora', Numeric(4, 2), server_default=text("'0.00'")),
    Column('valormora', Numeric(12, 2), server_default=text("'0.00'")),
    Column('percdesc', Numeric(4, 2), server_default=text("'0.00'")),
    Column('valordesc', Numeric(12, 2), server_default=text("'0.00'")),
    Column('deltitulo', Integer, server_default=text("'0'")),
    Column('numconta', Integer),
    Column('alt_venc', Integer, server_default=text("'0'")),
    Column('cod_ocorrencia', String(2))
)


t_vtab_suportes = Table(
    'vtab_suportes', metadata,
    Column('nome', String(255)),
    Column('email', String(255)),
    Column('vendedor', String(255)),
    Column('endereco', String(255)),
    Column('complemento', String(255)),
    Column('bairro', String(255)),
    Column('cidade', String(255)),
    Column('cep', String(9)),
    Column('estado', String(2)),
    Column('cpf_cnpj', String(20)),
    Column('fone', String(50)),
    Column('login', String(64)),
    Column('venc', String(2), server_default=text("'01'")),
    Column('celular', String(50)),
    Column('conta', String(11), server_default=text("'1'")),
    Column('plano', String(255)),
    Column('numero', String(20)),
    Column('cli_ativado', Enum('s', 'n'), server_default=text("'s'")),
    Column('bloqueado', String(3), server_default=text("'nao'")),
    Column('grupo', String(50)),
    Column('codigo', String(50)),
    Column('mesref', Enum('now', 'ant'), server_default=text("'ant'")),
    Column('assunto', String(255)),
    Column('abertura', DateTime),
    Column('fechamento', DateTime),
    Column('status', String(255), server_default=text("'aberto'")),
    Column('chamado', String(255)),
    Column('atendente', String(255)),
    Column('visita', DateTime),
    Column('prioridade', String(20), server_default=text("'normal'")),
    Column('ramal', String(20), server_default=text("'todos'")),
    Column('reply', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('tecnico', Integer),
    Column('login_atend', String(63), server_default=text("'full_users'")),
    Column('id', Integer, server_default=text("'0'"))
)


t_vtab_titulos = Table(
    'vtab_titulos', metadata,
    Column('nome', String(255)),
    Column('pessoa', String(10), server_default=text("'fisica'")),
    Column('nome_res', String(255)),
    Column('senha', String(255)),
    Column('email', String(255)),
    Column('vendedor', String(255)),
    Column('endereco', String(255)),
    Column('complemento', String(255)),
    Column('bairro', String(255)),
    Column('cidade', String(255)),
    Column('cep', String(9)),
    Column('estado', String(2)),
    Column('cpf_cnpj', String(20)),
    Column('fone', String(50)),
    Column('login', String(64)),
    Column('venc', String(2), server_default=text("'01'")),
    Column('celular', String(50)),
    Column('conta', String(11), server_default=text("'1'")),
    Column('plano', String(255)),
    Column('numero', String(20)),
    Column('desconto', Numeric(12, 2), server_default=text("'0.00'")),
    Column('acrescimo', Numeric(12, 2), server_default=text("'0.00'")),
    Column('ramal', String(255)),
    Column('cli_ativado', Enum('s', 'n'), server_default=text("'s'")),
    Column('bloqueado', String(3), server_default=text("'nao'")),
    Column('grupo', String(50)),
    Column('codigo', String(50)),
    Column('calculado', String(50)),
    Column('tags', String),
    Column('comodato', String(3), server_default=text("'nao'")),
    Column('dias_corte', Integer, server_default=text("'999'")),
    Column('geranfe', Enum('sim', 'nao'), server_default=text("'sim'")),
    Column('mesref', Enum('now', 'ant'), server_default=text("'ant'")),
    Column('opcelular', String(100), server_default=text("'nenhuma'")),
    Column('valor', String(50)),
    Column('valorpag', String(50)),
    Column('valorger', String(20), server_default=text("'completo'")),
    Column('formapag', String(100)),
    Column('linhadig', String(255)),
    Column('codigo_barras', String(80)),
    Column('datavenc', DateTime),
    Column('referencia', String(8)),
    Column('nossonum', String(64)),
    Column('datapag', DateTime),
    Column('recibo', String(255)),
    Column('status', String(255), server_default=text("'aberto'")),
    Column('tipo', String(255)),
    Column('processamento', DateTime),
    Column('usergerou', String(20)),
    Column('coletor', String(20)),
    Column('tipocob', Enum('fat', 'car'), server_default=text("'fat'")),
    Column('codigo_carne', String(32)),
    Column('fcartaobandeira', String(100)),
    Column('fcartaonumero', String(32)),
    Column('fchequenumero', String(100)),
    Column('fchequebanco', String(100)),
    Column('fchequeagcc', String(100)),
    Column('descricao', String(255)),
    Column('numconta', Integer),
    Column('num_retornos', Integer, server_default=text("'0'")),
    Column('deltitulo', Integer, server_default=text("'0'")),
    Column('gerourem', Enum('sim', 'nao'), server_default=text("'nao'")),
    Column('tarifa_paga', Numeric(12, 2), server_default=text("'0.00'")),
    Column('titulo', Integer, server_default=text("'0'")),
    Column('uuid_lanc', String(48)),
    Column('imp', Enum('sim', 'nao'), server_default=text("'nao'"))
)


t_vtab_usuarios = Table(
    'vtab_usuarios', metadata,
    Column('usuario', String(64))
)
